#!/bin/bash
# Agent 05 PR #5 — Merge Commands
# Status: Ready for merge to main
# Branch: feat/05-backend-gateway

echo "=========================================="
echo "Agent 05 PR #5 — Merge to Main"
echo "=========================================="
echo ""

# Step 1: Fetch latest from origin
echo "Step 1: Fetching latest from origin..."
git fetch origin
echo "✓ Done"
echo ""

# Step 2: Switch to main
echo "Step 2: Switching to main branch..."
git checkout main
echo "✓ Done"
echo ""

# Step 3: Pull latest main
echo "Step 3: Pulling latest main..."
git pull origin main
echo "✓ Done"
echo ""

# Step 4: Squash merge feature branch
echo "Step 4: Squash merging feat/05-backend-gateway..."
git merge --squash feat/05-backend-gateway
echo "✓ Done"
echo ""

# Step 5: Commit with conventional commit message
echo "Step 5: Committing with conventional message..."
git commit -m "feat(api): expose REST health/config and WS topics with schema validation

- Add FastAPI REST endpoints: /health, /health/ollama, /config
- Implement WebSocket endpoint with handshake, heartbeat, and message routing
- Create 20+ Pydantic models aligned with TypeScript contracts
- Add structured JSON logging with configurable format and level
- Implement environment-based configuration with .env support
- Create WebSocket connection manager for lifecycle and routing
- Add comprehensive test suite: 28 tests (health, WebSocket, legacy)
- All tests passing on Windows 11 with Python 3.11
- Include documentation: API summary, handoff to Agent 06, supervisor report

Acceptance Criteria:
- ✅ OpenAPI schema valid
- ✅ Health endpoint returns 200
- ✅ WebSocket integration smoke tests pass
- ✅ All pytest tests green (28/28)
- ✅ REST + WS round-trip tested
- ✅ Structured logging implemented
- ✅ Configuration system working
- ✅ Schema validation with Pydantic

Closes #5"
echo "✓ Done"
echo ""

# Step 6: Push to main
echo "Step 6: Pushing to main..."
git push origin main
echo "✓ Done"
echo ""

# Step 7: Delete feature branch locally
echo "Step 7: Deleting feature branch locally..."
git branch -d feat/05-backend-gateway
echo "✓ Done"
echo ""

# Step 8: Delete feature branch on origin
echo "Step 8: Deleting feature branch on origin..."
git push origin --delete feat/05-backend-gateway
echo "✓ Done"
echo ""

# Step 9: Verify merge
echo "Step 9: Verifying merge..."
echo "Recent commits:"
git log --oneline -5
echo ""

# Step 10: Run tests to verify
echo "Step 10: Running tests to verify..."
cd backend
python -m pytest tests/ -v --tb=short
echo ""

echo "=========================================="
echo "✅ Merge Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "- Feature branch merged to main"
echo "- Feature branch deleted locally and on origin"
echo "- All tests passing"
echo ""
echo "Next steps:"
echo "1. Share handoff document with Agent 06"
echo "2. Start Agent 06 — Indexing Service"
echo ""
