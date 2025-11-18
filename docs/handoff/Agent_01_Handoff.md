# Agent 01 Handoff — Extension Views & Commands

## Scope delivered
- Strict TypeScript config with path aliases (`@/*`).
- ESLint (type-aware) + Prettier; scripts for `lint`, `lint:fix`, `typecheck`, `format`, `format:check`.
- Jest baseline with coverage thresholds and an activation test.
- VS Code debug: Run Extension (preLaunch builds).
- CI: Windows + Ubuntu with npm caching; typecheck, lint, compile, tests, coverage artifact upload.

## How to run (local)
- Node 20.x, VS Code ≥ 1.88
- Commands (in `extension/`):
  - `npm ci`
  - `npm run typecheck`
  - `npm run lint` (or `npm run lint:fix`)
  - `npm run format:check` (or `npm run format`)
  - `npm run compile`
  - `npm run test:ci`
- Debug: VS Code launch → "Run Extension"

## Structure
- `src/extension.ts` — activation scaffold
- `__tests__/extension.test.ts` — smoke test
- `__mocks__/vscode.ts` — Jest mock
- `jest.config.js` — coverage + moduleNameMapper for `@/*` and `vscode`

## Notes
- Prettier enforces LF via `.prettierrc.json` and `.gitattributes` to keep CI consistent across OS.
- Thresholds are modest; can be raised when more tests land.
