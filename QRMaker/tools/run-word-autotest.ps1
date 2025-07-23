param(
  [string]$ManifestPath = "QRMaker\manifest.xml",
  [string]$DestRoot = "$env:USERPROFILE\Applications\Coding\Word_Addins\QRMaker"
)

Write-Host "=== QRMaker Word Autotest ==="

# Resolve full paths
$manifestFull = Resolve-Path $ManifestPath
$repoRoot = (Resolve-Path "..").Path
$repoRoot = Split-Path $PSScriptRoot -Parent   # repo root (one level up from tools)
Set-Location $repoRoot                         # run everything from repo root

# Ensure destination directory exists
if (!(Test-Path $DestRoot)) { New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null }

Write-Host "Copying add-in files to sideload folder..."
Copy-Item -Path "QRMaker\*" -Destination $DestRoot -Recurse -Force

# Replace manifest in dest root (Office looks for manifest there)
Copy-Item -Path $manifestFull -Destination $DestRoot -Force

# Ensure port 4201 free
$port = 4201
$busy = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($busy) {
  Write-Host "Port $port in use - terminating existing listener..."
  $busy | Select-Object -ExpandProperty OwningProcess | ForEach-Object {
    try { Get-Process -Id $_ -ErrorAction SilentlyContinue | Stop-Process -Force } catch {}
  }
  # wait until port truly free
  $attempt=0
  while (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue -Quiet -ne $null -and $attempt -lt 10) {
    Start-Sleep -Milliseconds 500
    $attempt++
  }
}

# Start local HTTPS result server for results (runs until it exits with code)
Write-Host "Starting local HTTPS result server..."
$serverLogOut = Join-Path $DestRoot "server_out.log"
$serverLogErr = Join-Path $DestRoot "server_err.log"

$nodeProc = Start-Process -FilePath "node" `
    -ArgumentList "tests/word/local-autotest-server.js" `
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

# Launch Word (empty)
Write-Host "Launching Word with blank document..."
Start-Process "winword.exe" "/n"

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