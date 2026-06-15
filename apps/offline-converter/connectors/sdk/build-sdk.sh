#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/dist/sdk"

rm -rf "$OUTPUT_DIR/PageMintConnector.sdk"
mkdir -p "$OUTPUT_DIR"
cp -R "$SCRIPT_DIR/PageMintConnector.sdk" "$OUTPUT_DIR/PageMintConnector.sdk"

echo "Created $OUTPUT_DIR/PageMintConnector.sdk"
