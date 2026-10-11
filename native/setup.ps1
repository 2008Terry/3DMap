$ErrorActionPreference = "Stop"

$nativeDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $nativeDir
$venvPython = Join-Path $nativeDir ".venv\Scripts\python.exe"
$pythonExe = $env:LOCAL_PYTHON

if (-not $pythonExe -or -not (Test-Path -LiteralPath $pythonExe)) {
    if (Test-Path -LiteralPath "D:\Terry\python.exe") {
        $pythonExe = "D:\Terry\python.exe"
    } else {
        $launcher = Get-Command py -ErrorAction SilentlyContinue
        if (-not $launcher) {
            throw "Python 3.12 was not found. Set LOCAL_PYTHON to its python.exe path."
        }
        $pythonExe = $launcher.Source
    }
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    if ((Split-Path -Leaf $pythonExe) -eq "py.exe") {
        & $pythonExe -3.12 -m venv --system-site-packages (Join-Path $nativeDir ".venv")
    } else {
        & $pythonExe -m venv --system-site-packages (Join-Path $nativeDir ".venv")
    }
    if ($LASTEXITCODE -ne 0) { throw "Could not create native/.venv with $pythonExe" }
}

& $venvPython -m pip install --disable-pip-version-check --no-deps -r (Join-Path $nativeDir "requirements.txt")
if ($LASTEXITCODE -ne 0) { throw "Could not install native runtime requirements." }

Write-Host "Native map environment is ready. Launch with .\native\run.ps1"
