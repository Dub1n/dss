param(
  # Path to the manifest; defaults to the manifest in the QRMaker folder one level up.
  [string]$ManifestPath = (Join-Path (Split-Path $PSScriptRoot -Parent) "manifest.xml"),

  # Destination root for sideloaded files (defaults to a temp directory)
  [string]$DestRoot = (Join-Path $env:TEMP "qr_addin_sideload"),

  # Word document to open for tests (defaults to project template)
  [string]$DocPath = (Join-Path (Split-Path $PSScriptRoot -Parent) "assets\qr_template.docx")
)

Write-Host "=== QRMaker Word Autotest ==="

# Resolve full paths
$manifestFull = Resolve-Path $ManifestPath
# repoRoot = QRMaker folder (parent of this tools directory)
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot                         # run everything from repo root

# Ensure destination directory exists
if (!(Test-Path $DestRoot)) { New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null }

Write-Host "Copying add-in files to sideload folder..."
Copy-Item -Path (Join-Path $repoRoot '*') -Destination $DestRoot -Recurse -Force

# Replace manifest in dest root (Office looks for manifest there)
Copy-Item -Path $manifestFull -Destination $DestRoot -Force

$port = 4201
function Test-PortFree($p) {
  return -not (Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue)
}

while (-not (Test-PortFree $port)) {
  Write-Host "Port $port is busy – attempting to free it..."
  $busyConns = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
  foreach ($conn in $busyConns) {
    if ($conn.OwningProcess -gt 0) {
      try { Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force } catch {}
    }
  }
  Start-Sleep -Milliseconds 500
  if (-not (Test-PortFree $port)) {
    Write-Host "Unable to free port $port, trying next port..."
    $port++
  }
}

# Export the chosen port for node server
$env:PORT = $port
Write-Host "Using free port $port for autotest server."

# Start local HTTPS result server for results (runs until it exits with code)
Write-Host "Starting local HTTPS result server..."
$serverLogOut = Join-Path $DestRoot "server_out.log"
$serverLogErr = Join-Path $DestRoot "server_err.log"

$nodeProc = Start-Process -FilePath "node" `
    -ArgumentList "tools/local-autotest-server.js" `
    -WorkingDirectory $repoRoot `
    -RedirectStandardOutput $serverLogOut `
    -RedirectStandardError $serverLogErr `
    -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3

if ($nodeProc.HasExited) {
  Write-Host "Server failed to start. Log output:" -ForegroundColor Red
  if (Test-Path $serverLogErr) { Get-Content $serverLogErr }
  else { Write-Host "(no log content)" }
  exit 1
}

# Kill any existing Word processes
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force

# ─────────────────────────────────────────────────────────────
# Update manifest copy to point at chosen port and ?autotest
# -----------------------------------------------------------------------------
$manifestCopy = Join-Path $DestRoot (Split-Path $manifestFull -Leaf)
[xml]$xml = Get-Content $manifestCopy

# Build namespace manager once
$nsMgr = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$nsMgr.AddNamespace("ov", "http://schemas.microsoft.com/office/taskpaneappversionoverrides")
$nsMgr.AddNamespace("bt", "http://schemas.microsoft.com/office/officeappbasictypes/1.0")

# Update SourceLocation / Taskpane.Url
$srcNodes = $xml.SelectNodes("//ov:SourceLocation | //bt:Url[@id='Taskpane.Url']", $nsMgr)
foreach ($n in $srcNodes) { $n.DefaultValue = "https://localhost:$port/QRMaker/taskpane.html?autotest" }

# Ensure auto-show
$tpNode = $xml.SelectSingleNode("//ov:TaskpaneId", $nsMgr)
if ($tpNode) { $tpNode.InnerText = "Office.AutoShowTaskpaneWithDocument" }

$xml.Save($manifestCopy)

# Register and sideload
Write-Host "Registering and sideloading add-in..."
npx office-addin-dev-settings unregister $manifestCopy | Out-Null
npx office-addin-dev-settings register   $manifestCopy | Out-Null

# Disable live-reload for clean session
npx office-addin-dev-settings live-reload --disable $manifestCopy | Out-Null

Write-Host "Launching Word via sideload..."
Stop-Process WINWORD -Force
Start-Sleep -Seconds 2
npx office-addin-dev-settings sideload $manifestCopy --app Word --document (Resolve-Path $DocPath)

# Re-enable live-reload in finally block later

# Wait for node server to exit with results (max 120s timeout)
$counter = 0
while (-not $nodeProc.HasExited -and $counter -lt 120) {
  Start-Sleep -Seconds 1
  $counter++
}

$procObj = Get-Process -Id $nodeProc.Id -ErrorAction SilentlyContinue
$exitCode = if ($procObj) { $procObj.ExitCode } else { 1 }

# Close Word
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force

if ($exitCode -eq 0) {
  Write-Host "Autotest passed." -ForegroundColor Green
  exit 0
} else {
  Write-Host "Autotest failed -- see autotest_log.json." -ForegroundColor Red
  exit 1
} 