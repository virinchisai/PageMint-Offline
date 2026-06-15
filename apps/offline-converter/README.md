# PageMint Offline

PageMint Offline is a privacy-first, local-only document-to-Markdown app powered by
Microsoft MarkItDown. The app name, copy, and user experience are intentionally distinct
so it can be packaged as its own product while still crediting MarkItDown as the
conversion engine.

## What it does

- Upload or drag-drop multiple files.
- Detect the format for every file before conversion.
- Convert files offline with `MarkItDown().convert_local(...)`.
- Download either one combined Markdown file or a ZIP containing separate Markdown files.
- Name a conversion collection so combined exports have a clean cover heading.
- Include a conversion summary in separate ZIP exports.
- Show an in-app privacy policy page at `/privacy`.
- Avoid retaining uploads by storing them only in a temporary per-request directory.

## Run locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e "apps/offline-converter[test]"
markitdown-app
```

Open `http://127.0.0.1:8765`.

## Package targets

### Windows and macOS

Use the app as a bundled local server and wrap it with a native shell:

1. Build a Python runtime with this package installed.
2. Start `markitdown-app --port 8765` from the shell process.
3. Point the shell webview at `http://127.0.0.1:8765`.

Practical shell options:

- Electron: easiest installer story and file associations.
- Tauri: smaller desktop bundles, but Python sidecar setup takes more care.
- Briefcase: Python-native packaging if you want to keep the shell in Python.

### Android and Google Play

Android is the hard target because MarkItDown is Python and several optional converters
use native dependencies. Use one of these approaches:

- Chaquopy Android app: run the same Python backend in-process and show the UI in a
  WebView. This is the most direct path for an offline APK.
- Kivy or BeeWare: viable for a Python-native UI, but some MarkItDown optional
  dependencies may need per-architecture wheels or substitutions.

For the first Android version, ship the core text, HTML, CSV, JSON, XML, DOCX, PPTX,
XLSX, PDF, ZIP, and EPUB converters first. Treat audio transcription, Azure converters,
YouTube URLs, and LLM/OCR plugins as optional because they either need network access,
system binaries, or platform-specific runtime work.

Before submitting to Google Play:

1. Host a public, non-PDF privacy policy URL and enter it in Play Console.
2. Complete the Data safety form accurately for the final Android build.
3. Publish as an Android App Bundle (`.aab`).
4. Avoid using "Microsoft" or "MarkItDown" in the app title, icon, or developer name in
   a way that suggests official affiliation.

See `docs/play-store.md` for suggested listing copy and compliance notes.
See `docs/process-instructions.md` for the step-by-step path from this local app to a
Play Store-ready Android release.
See `docs/desktop-connectors.md` for Windows `.exe` and macOS `.pkg` connector packaging
for Codex, Claude Desktop, and Perplexity.

## API

`POST /api/detect`

Multipart form field: `files`.

Returns:

```json
{
  "files": [
    {
      "name": "example.pdf",
      "extension": ".pdf",
      "mimetype": "application/pdf",
      "charset": null
    }
  ]
}
```

`POST /api/convert`

Multipart form fields:

- `files`: one or more uploads
- `mode`: `combined` or `separate`

Returns `pagemint-combined.md` for combined mode and
`pagemint-separate.zip` for separate mode.
