# One-shot setup for Windows PowerShell. Run from the repo root:
#   .\setup.ps1
# If scripts are blocked:  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Sets up the backend (venv, dependencies, migrations, seed data, tests)
# and the frontend (npm dependencies).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$repoRoot = $PSScriptRoot

$py = $null
foreach ($candidate in @("py -3", "python3", "python")) {
    try {
        $version = Invoke-Expression "$candidate -c `"import sys; print(sys.version_info >= (3, 10))`"" 2>$null
        if ($version -eq "True") { $py = $candidate; break }
    } catch {}
}
if (-not $py) {
    Write-Error "Python 3.10 or newer is required. Install it from https://www.python.org/downloads/ and re-run .\setup.ps1"
}
Write-Host "Using: $(Invoke-Expression "$py --version")"

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "Node 20 or newer is required and npm was not found on PATH. Install it from https://nodejs.org/ and re-run .\setup.ps1"
}
$nodeMajor = [int](node -p "process.versions.node.split('.')[0]")
if ($nodeMajor -lt 20) {
    Write-Error "Node 20 or newer is required; found $(node --version). Install it from https://nodejs.org/ and re-run .\setup.ps1"
}
Write-Host "Using node: $(node --version)"

Write-Host ""
Write-Host "Backend..."
Set-Location (Join-Path $repoRoot "backend")
if (-not (Test-Path ".venv")) { Invoke-Expression "$py -m venv .venv" }
& .\.venv\Scripts\Activate.ps1

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

Set-Location "src"
python manage.py migrate --verbosity 0
python manage.py seed_data

Set-Location ".."
# The API test is an unimplemented stub, so a failing test here is expected.
# Anything other than "tests ran and some failed" is a real setup problem.
$ErrorActionPreference = "Continue"
python -m pytest
$pytestStatus = $LASTEXITCODE
$ErrorActionPreference = "Stop"
if ($pytestStatus -gt 1) {
    Write-Error "pytest could not run. The backend is not set up correctly."
}

Write-Host ""
Write-Host "Frontend..."
Set-Location $repoRoot
npm install --prefix frontend

Write-Host ""
Write-Host "Setup complete."
Write-Host ""
Write-Host "One test fails: tests/test_purchase_request_api.py is an unimplemented stub"
Write-Host "and is yours to write. Everything else passes. See backend/README.md."
Write-Host ""
Write-Host "Next:"
Write-Host "  make dev"
Write-Host ""
Write-Host "  Frontend  http://localhost:5173"
Write-Host "  API       http://localhost:8000/api/purchase-requests/"
