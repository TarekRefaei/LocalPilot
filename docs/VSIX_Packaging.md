# VSIX Packaging (Windows)

Package the LocalPilot VS Code extension into a .vsix and install locally on Windows.

## Prerequisites
- Node.js 20.x
- VS Code ≥ 1.88
- vsce (VS Code Extension Manager)

Install vsce:
```powershell
npm i -g @vscode/vsce
# or project-local (dev dep): npm i -D @vscode/vsce
```

## Prepare the Extension
```powershell
cd extension
npm ci
npm run compile
```

Verify engine compatibility (extension/package.json):
- `engines.vscode` should be `^1.88.0` or higher, matching your VS Code.

## Package
```powershell
# from repo root or extension folder
cd extension
# Bump version in package.json when appropriate (semver)
# Then:
vsce package
```

Output:
- A file like `localpilot-0.0.1.vsix` is created in the `extension` folder.

## Install Locally
- Via command line:
```powershell
code --install-extension .\localpilot-0.0.1.vsix
```
- Or via VS Code UI:
  - Extensions panel → ... menu → Install from VSIX → select the `.vsix`

Restart VS Code if prompted.

## Smoke Test
- Start backend: http://127.0.0.1:8765
- Open the LocalPilot container in the Activity Bar
- Open Chat and send a short prompt → should stream echo

## Troubleshooting
- "Unsupported engine" → update `engines.vscode` or use matching VS Code version
- Packaging error about publisher → ensure `publisher` is set in `extension/package.json`
- Missing files → verify `files` field if used, or .vscodeignore content

## Release Checklist Tie-in
- Update `CHANGELOG.md`
- Ensure tests pass on CI
- Link packaging results in PR (artifact name and version)

See also: `docs/Release_Checklist.md`
