# PageMint Connector SDK

This SDK bundle contains the files needed to integrate PageMint Offline with desktop AI
clients through MCP.

## Connector Tool

The connector exposes one MCP tool:

```text
convert_to_markdown(uri)
```

Supported URI schemes:

- `file:`
- `http:`
- `https:`
- `data:`

## Install Targets

Windows connector executable:

```text
C:\Program Files\PageMint\PageMintConnector.exe
```

macOS connector command:

```text
/usr/local/bin/pagemint-connector
```

## Included Templates

- Claude Desktop config for Windows and macOS.
- Codex MCP config for Windows and macOS.
- Perplexity macOS command value.
- Tool manifest describing the MCP surface.

## Security

The connector runs locally with the current user's file permissions. AI tools connected
to it may request conversion of files that the current user can read. Use it only with
trusted desktop AI clients.
