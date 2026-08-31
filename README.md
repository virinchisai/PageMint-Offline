# PageMint Offline

[![Knowledge Reliability](https://github.com/virinchisai/PageMint-Offline/actions/workflows/knowledge-reliability.yml/badge.svg)](https://github.com/virinchisai/PageMint-Offline/actions/workflows/knowledge-reliability.yml)

PageMint Offline is a privacy-focused local document-to-Markdown converter built on
[Microsoft MarkItDown](https://github.com/microsoft/markitdown). It accepts mixed file
batches, detects formats locally, and exports either one combined Markdown document or a
ZIP containing separate Markdown files.

PageMint is an independent project and is not affiliated with, endorsed by, or sponsored
by Microsoft.

## Features

- Local conversion with no account, analytics, or cloud upload.
- Drag-and-drop or file-picker uploads.
- Automatic format detection.
- Combined Markdown and separate ZIP export modes.
- PDF, DOCX, PPTX, XLS, XLSX, HTML, CSV, JSON, XML, text, ZIP, and EPUB support.
- Localhost-only desktop launcher.
- Optional MCP connector for trusted desktop AI clients.

## Run From Source

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e "apps/offline-converter[test]"
pytest apps/offline-converter/tests
markitdown-app
```

Open `http://127.0.0.1:8765`.

## Security Model

- The web server binds to `127.0.0.1` by default and accepts only localhost host headers.
- Uploads are stored in a temporary per-request directory and removed after processing.
- Requests are limited to 250 MB and 50 files by default.
- Plugins are disabled in the local converter.
- Browser responses use a restrictive content security policy and disable caching.
- The MCP connector can access files readable by the current user. Connect it only to
  trusted desktop AI clients.

Do not expose the local web server to a public network. See [SECURITY.md](SECURITY.md) for
reporting instructions and supported security assumptions.

## Packaging

macOS build scripts are under `apps/offline-converter/connectors/macos`. Generated
installers are intentionally excluded from Git because they must be signed and notarized
before public distribution.

Windows connector binaries must be built on Windows. The Android/Play Store package is
not implemented yet; the current Android notes describe a future packaging path.

## Licensing

This repository is distributed under the MIT License. MarkItDown is an external
MIT-licensed dependency. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
