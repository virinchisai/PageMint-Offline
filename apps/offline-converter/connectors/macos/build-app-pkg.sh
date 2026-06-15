#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
OUTPUT_DIR="${1:-dist/macos-app}"
VENV="$REPO_ROOT/.venv-pagemint-app-macos"
PYTHON="$VENV/bin/python"
ROOT_DIR="$REPO_ROOT/build/pagemint-offline-app-pkg-root"
STATIC_DIR="$REPO_ROOT/apps/offline-converter/src/markitdown_app/static"
ENTRYPOINT="$REPO_ROOT/apps/offline-converter/src/markitdown_app/desktop_app.py"

cd "$REPO_ROOT"

if [ ! -x "$PYTHON" ]; then
  python3 -m venv "$VENV"
fi

"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install pyinstaller
"$PYTHON" -m pip install -e "apps/offline-converter"

"$PYTHON" -m PyInstaller \
  --noconfirm \
  --windowed \
  --name "PageMint Offline" \
  --collect-all magika \
  --collect-all markitdown \
  --add-data "$STATIC_DIR:markitdown_app/static" \
  --distpath "$OUTPUT_DIR" \
  --workpath "build/pagemint-offline-app-macos" \
  --specpath "build/pagemint-offline-app-macos" \
  "$ENTRYPOINT"

rm -rf "$ROOT_DIR"
mkdir -p "$ROOT_DIR/Applications"
cp -R "$OUTPUT_DIR/PageMint Offline.app" "$ROOT_DIR/Applications/PageMint Offline.app"

pkgbuild \
  --root "$ROOT_DIR" \
  --identifier "com.pagemint.offline.app" \
  --version "0.1.0" \
  --install-location "/" \
  "$OUTPUT_DIR/PageMintOfflineApp.pkg"

echo "Created $OUTPUT_DIR/PageMint Offline.app"
echo "Created $OUTPUT_DIR/PageMintOfflineApp.pkg"
