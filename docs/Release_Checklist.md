# Release Checklist (MVP v0.1)

## Pre-release Gates
- [ ] All milestones complete (Weeks 1–10)
- [ ] Coverage ≥ 85% overall; critical folders ≥ 85%
- [ ] Type coverage 100%; no TS compile warnings
- [ ] ESLint/ruff/flake8 clean; no high severity issues
- [ ] Views/Chat integration tests pass on CI
- [ ] Nightly E2E green for 5 consecutive days

## Packaging
- [ ] VS Code engine pinned to ≥ 1.88 in extension package.json
- [ ] Version bump (semver), changelog updated
- [ ] VSIX built and smoke-tested on Windows

## Documentation
- [ ] Master_Implementation_Plan.md current
- [ ] Technical_Architecture.md diagrams in sync
- [ ] Development_guide.md updated for Windows steps
- [ ] Testing_Strategy.md updated and examples compile
- [ ] ADRs recorded; Glossary updated

## Verification
- [ ] Windows onboarding from scratch succeeds
- [ ] Indexing sample repo < 15 min; retrieval quality meets targets
- [ ] Chat grounded by RAG; Plan and Act workflows verified (dry-run + apply + rollback)

## Post-release
- [ ] Tag release in Git
- [ ] Create GitHub release notes
- [ ] Open “Post-MVP Backlog” tracking issues
