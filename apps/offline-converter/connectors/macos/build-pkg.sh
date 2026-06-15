#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
OUTPUT_DIR="${1:-dist/macos}"
VENV="$REPO_ROOT/.venv-connector-macos"
PYTHON="$VENV/bin/python"
ROOT_DIR="$REPO_ROOT/build/pagemint-pkg-root"

cd "$REPO_ROOT"

if [ ! -x "$PYTHON" ]; then
  python3 -m venv "$VENV"
fi

"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install pyinstaller
"$PYTHON" -m pip install typer
"$PYTHON" -m pip install -e "apps/offline-converter[connectors]"

"$PYTHON" -m PyInstaller \
  --onefile \
  --console \
  --name pagemint-connector \
  --collect-all magika \
  --collect-all markitdown \
  --collect-all markitdown_mcp \
  --collect-all mcp \
  --distpath "$OUTPUT_DIR" \
  --workpath "build/pagemint-connector-macos" \
  --specpath "build/pagemint-connector-macos" \
  "apps/offline-converter/connectors/macos/run_pagemint_connector.py"

rm -rf "$ROOT_DIR"
mkdir -p "$ROOT_DIR/usr/local/bin"
cp "$OUTPUT_DIR/pagemint-connector" "$ROOT_DIR/usr/local/bin/pagemint-connector"
chmod 755 "$ROOT_DIR/usr/local/bin/pagemint-connector"

pkgbuild \
  --root "$ROOT_DIR" \
  --identifier "com.pagemint.connector" \
  --version "0.1.0" \
  --install-location "/" \
  "$OUTPUT_DIR/PageMintConnector.pkg"

echo "Created $OUTPUT_DIR/PageMintConnector.pkg"
