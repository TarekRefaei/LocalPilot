### Document 3: TROUBLESHOOTING.md

**Location:** `docs/ProjectDocuments/troubleshooting.md`

**Purpose:** Common issues and solutions for developers and users

**Content Required:**

# LocalPilot - Troubleshooting Guide

## Connection Issues

### "Cannot connect to Ollama"
**Symptoms:** Extension shows Ollama as disconnected
**Solutions:**
1. Verify Ollama is running: `curl http://localhost:11434/api/version`
2. Check system tray for Ollama icon
3. Restart Ollama: Close from tray → Start from Start Menu
4. Check firewall isn't blocking port 11434

### "Python server not responding"
**Symptoms:** Extension shows server as disconnected
**Solutions:**
1. Ensure server is running: `curl http://localhost:8000/health`
2. Check virtual environment is activated
3. Check port 8000 isn't used: `netstat -an | findstr 8000`
4. Review logs: `~/.localpilot/logs/server.log`

## Indexing Issues

### "Indexing is very slow"
**Causes:**
- Large files being processed
- Many files in workspace
- Ollama overloaded

**Solutions:**
1. Check `.gitignore` excludes `node_modules`, `dist`, etc.
2. Add large binary files to exclude patterns
3. Ensure embedding model is loaded: `ollama list`

### "Some files weren't indexed"
**Check:** Look at indexing summary for skipped files
**Common reasons:**
- File too large (>1MB)
- Unsupported extension
- Parse error (syntax issues)

## Chat Issues

### "Responses seem unrelated to my code"
**Solutions:**
1. Sync index if files changed: Click "Sync Index"
2. Check if relevant files are in supported languages
3. Be more specific in queries (mention file names)

### "Chat is very slow"
**Causes:**
- Large context being processed
- Model loading for first request

**Solutions:**
1. First request is slow (model loading) - wait
2. Reduce `ragTopK` setting
3. Try smaller model

## Act Mode Issues

### "Generated code doesn't compile"
**Solutions:**
1. Review code before applying
2. Edit generated code in preview
3. Re-generate with more specific task description

### "Can't recover from failed task"
**Solutions:**
1. Check `.localpilot/backups/` for original files
2. Use VS Code's undo (Ctrl+Z) immediately after
3. Restore from backup folder manually

## Development Issues

### "TypeScript errors after pulling"
```bash
cd extension
pnpm install
pnpm run build
```

### "Python import errors"
```bash
cd server
.venv\Scripts\activate
uv pip install -e ".[dev]"
```

### "Extension not loading in debug"
1. Ensure `pnpm run build` completed
2. Check `dist/extension.js` exists
3. Check Output panel for errors