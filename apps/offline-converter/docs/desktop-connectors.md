# PageMint Desktop Connectors

PageMint can be exposed to desktop AI tools as a local MCP connector. This lets an AI
assistant ask PageMint to convert a local file URI, web URI, or data URI into Markdown.

The connector uses the existing `markitdown-mcp` server and exposes this MCP tool:

`convert_to_markdown(uri)`

Supported URI schemes:

- `file:`
- `http:`
- `https:`
- `data:`

## Important Security Note

The connector runs with the permissions of the current user. If an AI client is allowed
to call the connector, it can ask the connector to read files that the current user can
read. Keep it local, use trusted AI clients, and do not bind the connector to a public
network interface.

## Windows `.exe` Connector

Build the Windows connector executable from the repository root:

```powershell
apps\offline-converter\connectors\windows\build-exe.ps1
```

Expected output:

```text
dist\windows\PageMintConnector.exe
```

Recommended install location:

```text
C:\Program Files\PageMint\PageMintConnector.exe
```

The `.exe` runs a STDIO MCP server. Desktop AI clients start it when they need the
connector.

## macOS `.pkg` Connector

Build the macOS package from the repository root:

```bash
apps/offline-converter/connectors/macos/build-pkg.sh
```

Expected output:

```text
dist/macos/PageMintConnector.pkg
```

The package installs:

```text
/usr/local/bin/pagemint-connector
```

The installed command runs a STDIO MCP server. Desktop AI clients start it when they need
the connector.

## Connect to Claude Desktop

Claude Desktop uses an MCP JSON configuration.

macOS config path:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Windows config path:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

macOS config:

```json
{
  "mcpServers": {
    "pagemint": {
      "command": "/usr/local/bin/pagemint-connector",
      "args": []
    }
  }
}
```

Windows config:

```json
{
  "mcpServers": {
    "pagemint": {
      "command": "C:\\Program Files\\PageMint\\PageMintConnector.exe",
      "args": []
    }
  }
}
```

Restart Claude Desktop after editing the config. Then ask Claude to use the PageMint
connector to convert a `file:` URI to Markdown.

## Connect to Codex

Codex can use MCP servers from its config.

macOS:

```toml
[mcp_servers.pagemint]
command = "/usr/local/bin/pagemint-connector"
args = []
```

Windows:

```toml
[mcp_servers.pagemint]
command = "C:\\Program Files\\PageMint\\PageMintConnector.exe"
args = []
```

You can also add the connector with the Codex CLI if your Codex installation supports
MCP server management:

```bash
codex mcp add pagemint -- /usr/local/bin/pagemint-connector
```

On Windows, use the installed `.exe` path instead.

## Connect to Perplexity

Perplexity currently supports local MCP connectors in the macOS app. Install
`PageMintConnector.pkg`, then open Perplexity for Mac:

1. Open Settings.
2. Go to Connectors.
3. Install or enable the Perplexity helper if prompted.
4. Choose Add Connector.
5. Use the Simple tab.
6. Server name: `PageMint`.
7. Command:

```text
/usr/local/bin/pagemint-connector
```

Save and wait for the connector to show as running.

Windows Perplexity local MCP support may not be available in the same way. For Windows,
use Codex or Claude Desktop with the `.exe` connector unless Perplexity adds Windows local
MCP support.

## Config Templates

Templates are included here:

- `connectors/config/claude-desktop.windows.json`
- `connectors/config/claude-desktop.macos.json`
- `connectors/config/codex.windows.toml`
- `connectors/config/codex.macos.toml`
- `connectors/config/perplexity.macos-command.txt`

## SDK Bundle

The repository also includes a developer SDK bundle template:

```text
apps/offline-converter/connectors/sdk/PageMintConnector.sdk
```

Build/copy it into the release output folder with:

```bash
apps/offline-converter/connectors/sdk/build-sdk.sh
```

Expected output:

```text
dist/sdk/PageMintConnector.sdk
```

## Example Prompts

Claude Desktop, Codex, or Perplexity:

```text
Use PageMint to convert file:///Users/me/Documents/report.pdf to Markdown and summarize it.
```

```text
Use the PageMint connector to convert file:///C:/Users/me/Documents/report.docx to Markdown.
```

## Troubleshooting

If the connector does not appear:

- Confirm the executable path exists.
- Restart the AI desktop app.
- Run the connector manually from a terminal to check for dependency errors.
- Use the MCP Inspector to verify the connector exposes `convert_to_markdown`.

Manual connector test:

```bash
/usr/local/bin/pagemint-connector
```

Windows:

```powershell
& "C:\Program Files\PageMint\PageMintConnector.exe"
```

The process waits for MCP STDIO messages, so a blank terminal is normal.
