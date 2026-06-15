# PageMint Offline Play Store Notes

## Store identity

App title: `PageMint Offline`

Short description:

Private document-to-Markdown conversion for mixed files, processed on your device.

Full description:

PageMint Offline turns PDFs, Office documents, spreadsheets, HTML, CSV, JSON, text files,
ZIP archives, EPUBs, images, and supported audio files into clean Markdown. Add one file
or a mixed batch, let PageMint detect each format, then export one combined Markdown file
or a ZIP with separate outputs and a conversion summary.

Designed for private workflows, PageMint runs the conversion engine locally and does not
require an account for offline conversion. It is useful for research notes, knowledge
bases, receipts, document review, personal archives, and Markdown-first writing systems.

PageMint uses Microsoft MarkItDown as an open-source conversion engine. PageMint is not
affiliated with, endorsed by, or sponsored by Microsoft.

## Screenshot set

- Main upload screen with empty state.
- Mixed file queue after detection.
- Combined/separate output selector.
- Download complete state.
- In-app privacy policy screen.

## Data Safety draft

Use this only if the final Android build keeps the current offline behavior:

- Data collected: No user data collected.
- Data shared: No user data shared.
- Account creation: No.
- Data deletion request: Not applicable if no account or cloud storage is added.
- Files and documents: User-selected files are processed locally for conversion and
  deleted from temporary app storage after the conversion request finishes.

Update these answers before release if you add analytics, crash reporting, ads, cloud OCR,
sync, accounts, remote URLs, or any SDK that collects identifiers.

## Privacy policy checklist

- Use a public, non-PDF URL.
- Include the exact app name or developer name used in Play Console.
- Include support contact details.
- State what files are accessed and why.
- State retention and deletion behavior.
- Keep the in-app privacy page consistent with the hosted policy.

## Android packaging notes

For a Play Store build, prefer a native Android shell that hosts this UI and runs the
Python converter locally. Chaquopy is the most direct path because it can run Python in an
Android app process. Start with a smaller dependency profile instead of `markitdown[all]`
if native wheels are not available for every architecture.

Suggested first Android dependency set:

- Core: `beautifulsoup4`, `requests`, `markdownify`, `magika`, `charset-normalizer`,
  `defusedxml`
- Documents: `mammoth`, `python-pptx`, `pandas`, `openpyxl`, `xlrd`, `lxml`
- PDF: `pdfminer.six`, `pdfplumber`
- Archives and ebooks: built-in ZIP support plus EPUB dependencies from MarkItDown

Defer cloud and network-dependent capabilities for the first Play release.
