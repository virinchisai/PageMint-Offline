param(
    [string]$OutputDir = "dist\windows"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\..\.."
$Venv = Join-Path $RepoRoot ".venv-connector-windows"
$Python = Join-Path $Venv "Scripts\python.exe"

Set-Location $RepoRoot

if (!(Test-Path $Python)) {
    py -3.12 -m venv $Venv
}

& $Python -m pip install --upgrade pip
& $Python -m pip install pyinstaller
& $Python -m pip install typer
& $Python -m pip install -e "apps/offline-converter[connectors]"

& $Python -m PyInstaller `
    --onefile `
    --console `
    --name PageMintConnector `
    --collect-all magika `
    --collect-all markitdown `
    --collect-all markitdown_mcp `
    --collect-all mcp `
    --distpath $OutputDir `
    --workpath "build\pagemint-connector-windows" `
    --specpath "build\pagemint-connector-windows" `
    "apps\offline-converter\connectors\windows\run_pagemint_connector.py"

Write-Host "Created $OutputDir\PageMintConnector.exe"
