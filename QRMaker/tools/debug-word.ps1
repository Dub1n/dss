<#
.SYNOPSIS
  Launches a full local debug session for the QRMaker add-in:
  1. Trusts localhost dev cert (first run only)
  2. Registers QRMaker\manifest.xml with Word
  3. Starts HTTPS static server on https://localhost:4201
  4. Opens Word (tests\word\autotest.docx if it exists, else blank)
#>

param(
  [int]   $Port      = 4201,
  [string]$Manifest  = "manifest.xml",
  [string]$TestDoc   = "assets\qr_template.docx",
  [switch]$RunTests   # when provided (default behaviour), waits for autotest harness and propagates exit-code
)

$ErrorActionPreference = 'Stop'
$repoRoot = $PSScriptRoot | Split-Path -Parent
Set-Location $repoRoot

Write-Host "=== QRMaker Debug Launch ===`n"

# 0. Close Word if running
Write-Host "Step 0 : Closing Word if running..."
taskkill /IM WINWORD.EXE /F

# 1. Trust dev cert (only once)
Write-Host "Step 1 : Trusting localhost dev certificate (if needed)..."
npx office-addin-dev-certs install

# 2. Register manifest with Word
Write-Host "Step 2 : Registering manifest with Word dev-catalog..."
npx office-addin-dev-settings unregister $Manifest | Out-Null
npx office-addin-dev-settings register $Manifest | Out-Null

# 3. Disable live-reload (clean session)
Write-Host "Step 3 : Disabling live-reload (clean slate)..."
npx office-addin-dev-settings live-reload --disable $Manifest | Out-Null

# 4. Start debugging with DevTools
Write-Host "Step 4 : Starting debugging..."
npx office-addin-dev-settings debugging --open-dev-tools --enable $Manifest

# 5. Start HTTPS static server
Write-Host "Step 5 : Starting HTTPS static server on https://localhost:$Port"
$env:PORT = $Port
$server = Start-Process -FilePath "node" `
          -ArgumentList "tools/local-autotest-server.js" `
          -WorkingDirectory $repoRoot `
          -PassThru -WindowStyle Normal

Start-Sleep 2
if ($server.HasExited) {
  Write-Error "Server failed to start (exit $($server.ExitCode))."
  Exit 1
}

# ─────────────────────────────────────────────────────────────────────────────
# (Optional) Pure-Node unit tests
# -----------------------------------------------------------------------------
try {
  Write-Host "Running Node unit tests (tests/run_tests.js)…"
  & node "tests/run_tests.js"
  if ($LASTEXITCODE -ne 0) {
    throw "Node unit tests failed with exit code $LASTEXITCODE"
  }
  Write-Host "Node unit tests passed."
} catch {
  Write-Error $_
  exit 1
}

# 6. Launch Word + test document via sideload
Write-Host "Step 6 : Launching Word..."
if (Test-Path $TestDoc) {
  npx office-addin-dev-settings sideload $Manifest --app Word --document (Resolve-Path $TestDoc)
  Write-Host "Opened test document: $TestDoc"
} else {
  Start-Process "winword.exe" "/n"
  Write-Host "(No pre-seeded doc found : opened blank document.)"
}

if ($PSBoundParameters.ContainsKey('RunTests')) {
  Write-Host "`nWaiting for Word autotests to finish…"
  Wait-Process -Id $server.Id

  $exitCode = $server.ExitCode
  Write-Host "`nAutotest server exited with code $exitCode"
} else {
  Write-Host "`nServer output will appear below. Press Ctrl-C to stop."
  Wait-Process -Id $server.Id
  $exitCode = 0
}

# ensure live-reload is switched back on regardless of test mode
if (-not $server.HasExited) { Stop-Process -Id $server.Id }
Write-Host "`nRe-enabling live-reload for convenience..."
npx office-addin-dev-settings live-reload --enable $Manifest | Out-Null
Write-Host "`nDebug session ended. Live-reload is ON."

exit $exitCode