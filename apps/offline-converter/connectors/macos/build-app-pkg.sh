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

if [ -n "${MACOS_SIGN_IDENTITY:-}" ]; then
  codesign \
    --force \
    --deep \
    --options runtime \
    --sign "$MACOS_SIGN_IDENTITY" \
    "$OUTPUT_DIR/PageMint Offline.app"
fi

if [ -n "${APPLE_ID:-}" ] && [ -n "${APPLE_TEAM_ID:-}" ] && [ -n "${APPLE_APP_PASSWORD:-}" ]; then
  APP_NOTARY_ZIP="$OUTPUT_DIR/PageMintOffline-notary.zip"
  ditto -c -k --sequesterRsrc --keepParent "$OUTPUT_DIR/PageMint Offline.app" "$APP_NOTARY_ZIP"
  xcrun notarytool submit "$APP_NOTARY_ZIP" \
    --apple-id "$APPLE_ID" \
    --team-id "$APPLE_TEAM_ID" \
    --password "$APPLE_APP_PASSWORD" \
    --wait
  xcrun stapler staple "$OUTPUT_DIR/PageMint Offline.app"
  rm -f "$APP_NOTARY_ZIP"
fi

rm -rf "$ROOT_DIR"
mkdir -p "$ROOT_DIR/Applications"
cp -R "$OUTPUT_DIR/PageMint Offline.app" "$ROOT_DIR/Applications/PageMint Offline.app"

PKGBUILD_ARGS=(
  --root "$ROOT_DIR" \
  --identifier "com.pagemint.offline.app" \
  --version "0.1.0" \
  --install-location "/"
)

if [ -n "${MACOS_INSTALLER_IDENTITY:-}" ]; then
  PKGBUILD_ARGS+=(--sign "$MACOS_INSTALLER_IDENTITY")
fi

pkgbuild "${PKGBUILD_ARGS[@]}" "$OUTPUT_DIR/PageMintOfflineApp.pkg"

if [ -n "${APPLE_ID:-}" ] && [ -n "${APPLE_TEAM_ID:-}" ] && [ -n "${APPLE_APP_PASSWORD:-}" ]; then
  xcrun notarytool submit "$OUTPUT_DIR/PageMintOfflineApp.pkg" \
    --apple-id "$APPLE_ID" \
    --team-id "$APPLE_TEAM_ID" \
    --password "$APPLE_APP_PASSWORD" \
    --wait
  xcrun stapler staple "$OUTPUT_DIR/PageMintOfflineApp.pkg"
fi

echo "Created $OUTPUT_DIR/PageMint Offline.app"
echo "Created $OUTPUT_DIR/PageMintOfflineApp.pkg"
