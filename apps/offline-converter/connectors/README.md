# PageMint MCP Connector

Convert PDFs, DOCX, PPTX, XLSX, HTML, CSV and more to compact Markdown — locally, with no cloud uploads — so AI tools consume clean text instead of binary blobs.

## How it works

`mcp_server.py` is a standalone [MCP](https://modelcontextprotocol.io) server built on `markitdown` + `mcp`. Any AI client that supports the Model Context Protocol can connect to it over stdio and call its tools.

### Tools exposed

| Tool | Args | Description |
|------|------|-------------|
| `convert_file_to_markdown` | `file_path` | Convert a local file to Markdown |
| `convert_url_to_markdown` | `url` | Download a remote document and convert it |
| `convert_base64_to_markdown` | `data`, `filename` | Convert a base64-encoded file (useful in API pipelines) |

### Token savings

A 10-page PDF as raw binary is unusable inside an LLM context. The same PDF converted to Markdown is ~2 000–5 000 tokens of clean, readable text — a 90 %+ reduction in wasted context.

---

## Installation

```bash
pip install markitdown[pdf] mcp
```

Then copy `mcp_server.py` anywhere convenient, e.g. `~/.pagemint/mcp_server.py`.

---

## Connecting to AI tools

### Claude Desktop

Copy the relevant file from `config/` into your Claude Desktop config:

**macOS** — edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "pagemint": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

**Windows** — edit `%APPDATA%\Claude\claude_desktop_config.json` the same way.

Restart Claude Desktop. A hammer icon appears when the connector is active.

**Example prompt:**
> Use PageMint to convert `/Users/me/Documents/report.pdf` and summarize the key findings.

---

### Claude Code (CLI)

Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "pagemint": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

---

### Cursor

Add to `.cursor/mcp.json` in your project root (or `~/.cursor/mcp.json` globally):
```json
{
  "mcpServers": {
    "pagemint": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

---

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "pagemint": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

---

### Codex (OpenAI CLI)

See `config/codex.macos.toml` / `config/codex.windows.toml`.

---

### ChatGPT

ChatGPT does not support MCP natively. Pre-convert your file locally and paste the Markdown:

```bash
python3 -c "
from markitdown import MarkItDown
print(MarkItDown().convert('report.pdf').text_content)
" | pbcopy   # copies to clipboard (macOS)
```

To expose PageMint as a **Custom GPT Action**, wrap `mcp_server.py` in a small FastAPI app and point the GPT action schema at your public endpoint.

---

## Pre-built connectors (macOS & Windows)

The `macos/` and `windows/` folders contain build scripts that compile `mcp_server.py` into a self-contained native executable (`pagemint-connector`) — no Python installation required on end-user machines.

See the `sdk/` folder for the distributable SDK bundle and manifest.
