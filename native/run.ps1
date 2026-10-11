$ErrorActionPreference = "Stop"

$nativeDir = $PSScriptRoot
$venvPython = Join-Path $nativeDir ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $venvPython)) {
    & (Join-Path $nativeDir "setup.ps1")
}

& $venvPython (Join-Path $nativeDir "main.py")
exit $LASTEXITCODE
