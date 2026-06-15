# PageMint Offline Process Instructions

This guide explains the process for turning PageMint Offline from the current working
local app into a Play Store-ready Android application.

## 1. Understand What Exists Now

PageMint Offline currently has:

- A local web interface for uploading one or more files.
- Automatic file format detection.
- Offline conversion through Microsoft MarkItDown.
- Two output modes:
  - Combined Markdown file.
  - Separate Markdown files in a ZIP.
- Branded PageMint UI and download names.
- An in-app privacy page.
- Play Store listing notes and a privacy policy draft.

The current app is not yet an Android APK or Android App Bundle. It is the product core
that needs to be wrapped inside an Android shell.

## 2. Recommended Android Packaging Path

Use a native Android project with a WebView UI and a local Python runtime.

Recommended option:

- Android Studio + Kotlin/Java shell.
- Chaquopy for running Python inside Android.
- WebView for showing the PageMint HTML/CSS/JS interface.
- Local bridge between WebView and Python conversion logic.

This keeps conversion offline and avoids needing a remote server.

## 3. Android Build Steps

1. Create a new Android Studio project.
2. Add Chaquopy to the Gradle configuration.
3. Copy the PageMint frontend files into Android assets:
   - `src/markitdown_app/static/index.html`
   - `src/markitdown_app/static/styles.css`
   - `src/markitdown_app/static/app.js`
   - `src/markitdown_app/static/privacy.html`
   - `src/markitdown_app/static/manifest.webmanifest`
4. Move the Python conversion logic from `markitdown_app/server.py` into Android Python
   modules.
5. Replace Flask upload endpoints with Android/WebView file picker calls.
6. Pass selected file paths from Android to Python.
7. Run MarkItDown conversion locally.
8. Save the generated Markdown or ZIP through Android's storage/share system.
9. Test on real Android devices.
10. Build a signed Android App Bundle (`.aab`) for Play Store upload.

## 4. Keep the First Android Version Focused

For the first Play Store release, support the most reliable offline formats first:

- PDF
- DOCX
- PPTX
- XLSX
- XLS
- CSV
- JSON
- XML
- HTML
- TXT
- ZIP
- EPUB

Delay these features until later:

- YouTube URL conversion.
- Azure cloud conversion.
- LLM image captioning.
- Cloud OCR.
- Account sync.
- Ads or analytics.

This makes the first release easier to approve and easier to explain in the Data Safety
form.

## 5. Privacy and Play Store Requirements

Before publishing:

1. Review the developer contact in:
   - `src/markitdown_app/static/privacy.html`
   - `docs/privacy-policy-draft.md`
2. Host the final privacy policy on a public website.
3. Add that privacy policy URL in Play Console.
4. Complete the Data Safety form truthfully.
5. Make sure the Play Store listing does not imply Microsoft owns or endorses the app.
6. Credit MarkItDown as the open-source conversion engine.

Suggested wording:

> PageMint uses Microsoft MarkItDown as an open-source conversion engine. PageMint is
> not affiliated with, endorsed by, or sponsored by Microsoft.

## 6. Store Listing Preparation

Use `docs/play-store.md` as the starting point for:

- App title.
- Short description.
- Full description.
- Screenshot checklist.
- Data Safety draft.
- Android packaging notes.

Recommended Play Store title:

`PageMint Offline`

Recommended short description:

`Private document-to-Markdown conversion for mixed files, processed on your device.`

## 7. Testing Checklist

Before uploading to Play Store, test:

- Single file conversion.
- Multiple file conversion.
- Mixed file types in one batch.
- Combined Markdown export.
- Separate ZIP export.
- Large files.
- Unsupported files.
- Files with spaces and special characters in names.
- Privacy page opens inside the app.
- App works without internet.
- App does not request unnecessary Android permissions.

## 8. Release Checklist

Before production release:

- App name finalized.
- App icon created.
- Feature graphic created.
- Screenshots created.
- Privacy policy hosted.
- Data Safety completed.
- Android App Bundle signed.
- Internal testing track completed.
- Closed or open testing completed if required by your Play Console account.
- Production release notes written.

## 9. Future Upgrade Ideas

After the first release is stable:

- Add recent conversion history stored only on device.
- Add share-to-PageMint from Android's share sheet.
- Add Markdown preview.
- Add dark mode.
- Add batch naming templates.
- Add desktop `.exe` and `.pkg` connector installers for Codex, Claude Desktop, and
  Perplexity.
- Add optional OCR pack if Android dependencies are reliable.
- Add Pro features only after the free offline workflow is solid.

## 10. Simple Mental Model

Think of the project in three layers:

1. Conversion engine: MarkItDown converts files to Markdown.
2. Product experience: PageMint gives the engine a unique privacy-first app identity.
3. Android packaging: Android Studio and Chaquopy turn PageMint into a Play Store app.

Do the work in that order. Keep the conversion local, keep the permissions minimal, and
make the privacy story easy for users and Google Play reviewers to understand.
