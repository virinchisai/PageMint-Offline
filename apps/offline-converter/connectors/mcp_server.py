#!/usr/bin/env python3
"""PageMint MCP server — converts PDFs and other documents to compact Markdown."""
from __future__ import annotations

import base64
import os
import tempfile
import urllib.request
import urllib.parse
from pathlib import Path

from markitdown import MarkItDown
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pagemint")
_converter = MarkItDown()


def _convert_path(path: str) -> str:
    result = _converter.convert(path)
    return result.text_content


@mcp.tool()
def convert_file_to_markdown(file_path: str) -> str:
    """Convert a local file (PDF, DOCX, PPTX, XLSX, HTML, CSV, etc.) to Markdown.

    Args:
        file_path: Absolute path to the file on disk.

    Returns:
        Markdown text extracted from the file.
    """
    p = Path(file_path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return _convert_path(str(p))


@mcp.tool()
def convert_url_to_markdown(url: str) -> str:
    """Fetch a URL and convert its content (PDF, HTML, etc.) to Markdown.

    Args:
        url: http:// or https:// URL of the document.

    Returns:
        Markdown text extracted from the remote document.
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are supported.")
    suffix = Path(parsed.path).suffix or ".html"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = tmp.name
    try:
        urllib.request.urlretrieve(url, tmp_path)
        return _convert_path(tmp_path)
    finally:
        os.unlink(tmp_path)


@mcp.tool()
def convert_base64_to_markdown(data: str, filename: str = "document.pdf") -> str:
    """Convert a base64-encoded file to Markdown. Useful when the AI receives a file as base64.

    Args:
        data: Base64-encoded file content.
        filename: Original filename (used to detect format, e.g. 'report.pdf').

    Returns:
        Markdown text extracted from the file.
    """
    suffix = Path(filename).suffix or ".pdf"
    raw = base64.b64decode(data)
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name
    try:
        return _convert_path(tmp_path)
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    mcp.run(transport="stdio")
