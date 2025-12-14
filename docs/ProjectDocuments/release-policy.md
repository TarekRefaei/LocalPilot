# LocalPilot – Release and Tagging Policy

## Goals
- Clear restore points per phase
- Verifiable milestones
- Safe reverts

## Tagging
- Use annotated tags for milestones and phases.
- Format: `v<major>.<minor>.<patch>-<label>`
  - Examples:
    - `v0.1.0-phase0` (Phase 0 complete)
    - `v0.2.0-phase1` (Phase 1 complete)
- Use signed tags if you maintain a GPG key: `git tag -s ...`

## Creating a tag
```
# Annotated tag
git tag -a v0.1.1 -m "Short description"

# Signed tag (optional)
git tag -s v0.1.1 -m "Short description"

# Push
git push origin --tags
```

## Phase boundaries
- At the end of each Phase:
  - Commit: `chore(phase<N>): lock Phase <N> implementation`
  - Tag: `v0.<N>.0-phase<N>`

## Reverting
- Use `git revert <sha>` on shared branches.
- To restore a prior state locally:
  - `git reset --hard v0.1.0-phase0`

## Releases (optional)
- GitHub releases can be created for phase tags.
- Include changelog summary and verification checklist.
