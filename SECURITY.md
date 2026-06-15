# Security Policy

## Reporting

Please do not open a public issue for an undisclosed vulnerability. Use GitHub's private
vulnerability reporting feature when it is enabled for this repository.

## Supported Use

PageMint Offline is designed for a single user on a trusted computer:

- Keep the server bound to `127.0.0.1`.
- Convert files you trust or process them in an isolated environment.
- Do not run PageMint as an administrator or root user.
- Connect the MCP connector only to trusted desktop AI clients.

Document conversion libraries parse complex, potentially hostile formats. Local-only
operation reduces network exposure but does not make untrusted files harmless.

## Distribution

The repository does not publish unsigned application installers. Public macOS releases
should be code-signed and notarized, and release artifacts should include checksums.
