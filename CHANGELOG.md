# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- CONTRIBUTING.md with Windows-friendly flow and quality gates.
- docs/Onboarding_Windows.md (≤ 15 min setup and launch).
- docs/VSIX_Packaging.md with packaging and install steps on Windows.

### Changed
- Standardized backend dev port to 8765 across README and VS Code configs.
- README settings aligned with extension default `localpilot.backend.baseUrl` (http://127.0.0.1:8765).

### Fixed
- VS Code debug/task configs using inconsistent port (switched 8000 → 8765).

## [0.0.1] - Initial MVP
- Initial repository scaffolding, extension and backend setup, CI workflows, and docs baseline.
