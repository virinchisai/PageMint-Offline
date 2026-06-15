# Releasing PageMint Offline

PageMint publishes source code in the repository and generated desktop builds through
GitHub Actions artifacts or GitHub Releases.

## Build Artifacts

The `Release Installers` workflow creates:

- `PageMintOfflineApp.pkg`: macOS installer that places `PageMint Offline.app` in
  `/Applications`.
- `PageMintOffline-macOS-app.zip`: zipped macOS app bundle for users who prefer manual
  drag-and-drop installation.
- `PageMintOffline-Windows-app.zip`: zipped Windows desktop executable.
- `PageMintOfflineSetup.exe`: Windows installer built with Inno Setup.
- `PageMintConnector-Windows.zip`: Windows MCP connector executable for trusted desktop
  AI clients.
- `SHA256SUMS-*.txt`: checksums for verifying downloads.

## Manual Build

macOS:

```bash
apps/offline-converter/connectors/macos/build-app-pkg.sh dist/macos-app
```

Windows:

```powershell
apps\offline-converter\connectors\windows\build-app-exe.ps1 -OutputDir dist\windows-app
choco install innosetup --no-progress -y
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" apps\offline-converter\connectors\windows\PageMintOffline.iss
```

## Publishing a Release

Create and push a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release workflow builds both platforms and creates a draft GitHub Release with the
generated artifacts attached.

## Signing Status

The default workflow produces unsigned builds. Unsigned builds are useful for testers, but
public users may see warnings:

- macOS may show an unidentified developer or damaged-app warning until builds are signed
  and notarized with an Apple Developer ID.
- Windows may show Microsoft Defender SmartScreen warnings until builds are signed and
  the publisher develops reputation.

Before broad public distribution, add platform signing:

- macOS: sign the `.app`, sign the `.pkg`, submit for notarization, staple the ticket, and
  publish checksums.
- Windows: sign the app `.exe` and installer `.exe` with an Authenticode code-signing
  certificate.

## Signing Secrets

The release workflow signs builds automatically when these repository secrets exist.

macOS:

- `MACOS_CERTIFICATE_BASE64`: base64 encoded `.p12` containing Developer ID certificates.
- `MACOS_CERTIFICATE_PASSWORD`: password for the `.p12`.
- `MACOS_SIGN_IDENTITY`: Developer ID Application identity name.
- `MACOS_INSTALLER_IDENTITY`: Developer ID Installer identity name.
- `APPLE_ID`: Apple Developer account email.
- `APPLE_TEAM_ID`: Apple Developer team ID.
- `APPLE_APP_PASSWORD`: app-specific password for notarization.

Windows:

- `WINDOWS_CERTIFICATE_BASE64`: base64 encoded `.pfx` code-signing certificate.
- `WINDOWS_CERTIFICATE_PASSWORD`: password for the `.pfx`.

Do not commit signing certificates, passwords, API keys, or notarization credentials.
