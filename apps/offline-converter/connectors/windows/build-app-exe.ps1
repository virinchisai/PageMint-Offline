param(
    [string]$OutputDir = "dist\windows-app"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path "$PSScriptRoot\..\..\..\.."
$Venv = Join-Path $RepoRoot ".venv-pagemint-app-windows"
$Python = Join-Path $Venv "Scripts\python.exe"

Set-Location $RepoRoot

if (!(Test-Path $Python)) {
    py -3.12 -m venv $Venv
}

& $Python -m pip install --upgrade pip
& $Python -m pip install pyinstaller
& $Python -m pip install -e "apps/offline-converter"

& $Python -m PyInstaller `
    --noconfirm `
    --windowed `
    --onefile `
    --name "PageMint Offline" `
    --collect-all magika `
    --collect-all markitdown `
    --collect-data markitdown_app `
    --distpath $OutputDir `
    --workpath "build\pagemint-offline-app-windows" `
    --specpath "build\pagemint-offline-app-windows" `
    "apps\offline-converter\src\markitdown_app\desktop_app.py"

Write-Host "Created $OutputDir\PageMint Offline.exe"
