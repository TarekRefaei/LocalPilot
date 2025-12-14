# 📄 SECURITY_MODEL.md

# LocalPilot - Security Model

> Workspace safety rules and security boundaries for LocalPilot

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Security Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Security Principles](#1-security-principles)
2. [Threat Model](#2-threat-model)
3. [Workspace Boundaries](#3-workspace-boundaries)
4. [Act Mode Security](#4-act-mode-security)
5. [File Operation Rules](#5-file-operation-rules)
6. [Validation Functions](#6-validation-functions)
7. [Audit & Logging](#7-audit--logging)
8. [Security Checklist](#8-security-checklist)

---

## 1. Security Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                   CORE SECURITY PRINCIPLES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRINCIPLE 1: LEAST PRIVILEGE                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  LocalPilot only accesses what it absolutely needs.            │
│  • Only workspace files (no system files)                       │
│  • Only explicit user-approved operations                       │
│  • No background file modifications                             │
│                                                                  │
│  PRINCIPLE 2: EXPLICIT CONSENT                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every file modification requires explicit user approval.       │
│  • Show diff before applying                                    │
│  • User clicks "Apply" for each change                          │
│  • Never auto-apply without confirmation                        │
│                                                                  │
│  PRINCIPLE 3: DEFENSE IN DEPTH                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Multiple layers of protection:                                 │
│  • Path validation at input                                      │
│  • Path validation at execution                                  │
│  • Backup before modification                                    │
│  • Audit log of all operations                                   │
│                                                                  │
│  PRINCIPLE 4: FAIL SECURE                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  When in doubt, deny the operation.                             │
│  • Invalid path? Reject.                                         │
│  • Suspicious pattern? Reject.                                   │
│  • Outside workspace? Reject.                                    │
│                                                                  │
│  PRINCIPLE 5: TRANSPARENCY                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  User sees everything LocalPilot does.                          │
│  • All operations logged                                         │
│  • No hidden file changes                                        │
│  • Clear error messages                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Threat Model

### 2.1 Identified Threats

| Threat | Severity | Mitigation |
|--------|----------|------------|
| **Path Traversal** | CRITICAL | Path validation, workspace boundary |
| **Arbitrary File Write** | CRITICAL | Allowlist paths, user approval |
| **Sensitive File Access** | HIGH | Block sensitive file patterns |
| **LLM Injection** | MEDIUM | Sanitize LLM output before use |
| **Denial of Service** | LOW | Rate limiting, timeouts |
| **Data Exfiltration** | LOW | Localhost-only communication |

### 2.2 Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRUST BOUNDARIES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TRUSTED:                                                        │
│  ├── User input (explicit commands)                             │
│  ├── VS Code APIs                                                │
│  └── Local file system (within workspace)                       │
│                                                                  │
│  PARTIALLY TRUSTED:                                              │
│  ├── Ollama responses (sanitize before file ops)                │
│  ├── Python server responses                                     │
│  └── LLM-generated code (require user approval)                 │
│                                                                  │
│  UNTRUSTED:                                                      │
│  ├── LLM-suggested file paths (validate strictly)               │
│  ├── LLM-suggested commands (block in MVP)                      │
│  └── Any path containing traversal patterns                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Workspace Boundaries

### 3.1 Workspace Root Definition

```typescript
// The workspace root is the ONLY allowed base directory
const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;

// All file operations MUST be within this boundary
// Exception: ~/.localpilot/ for index storage (read/write by server only)
```

### 3.2 Allowed Paths

```
┌─────────────────────────────────────────────────────────────────┐
│                      ALLOWED PATHS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ ALLOWED (Read & Write):                                     │
│  ├── {workspace}/**/*                                           │
│  ├── {workspace}/src/**/*                                       │
│  ├── {workspace}/lib/**/*                                       │
│  └── {workspace}/[any subfolder]/**/*                          │
│                                                                  │
│  ✅ ALLOWED (Read Only):                                        │
│  ├── {workspace}/node_modules/** (for indexing)                │
│  ├── {workspace}/.git/** (for future git integration)          │
│  └── {workspace}/package.json, etc.                            │
│                                                                  │
│  ❌ BLOCKED (Never Access):                                     │
│  ├── Anything outside {workspace}/                              │
│  ├── C:\Windows\**                                               │
│  ├── /etc/**                                                     │
│  ├── /usr/**                                                     │
│  ├── ~/** (except ~/.localpilot/ for server)                   │
│  └── Any absolute path not under workspace                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Blocked Patterns

```typescript
// BLOCKED_PATTERNS: Never allow these in any path
const BLOCKED_PATTERNS = [
  // Traversal attempts
  '..',
  '..\\',
  '../',
  
  // Sensitive files
  '.env',
  '.env.local',
  '.env.production',
  'secrets',
  'credentials',
  'private_key',
  'id_rsa',
  '.ssh',
  '.aws',
  '.azure',
  
  // System paths (Windows)
  'C:\\Windows',
  'C:\\Program Files',
  'System32',
  
  // System paths (Unix - for future)
  '/etc/',
  '/usr/',
  '/bin/',
  '/sbin/',
  '/var/',
  '/root/',
  
  // Git internals
  '.git/config',
  '.git/hooks',
  
  // Package manager internals
  'node_modules/.bin',
];
```

---

## 4. Act Mode Security

### 4.1 Act Mode Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACT MODE SECURITY RULES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RULE 1: No Auto-Execution                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every task requires explicit "Apply" click.                    │
│  Default: Show preview, wait for approval.                      │
│  Future setting: "Auto-approve" only for create (not modify).   │
│                                                                  │
│  RULE 2: Backup Before Modify                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Before ANY file modification:                                  │
│  1. Create backup in .localpilot/backups/{timestamp}/          │
│  2. Store original content                                       │
│  3. Then apply changes                                           │
│  4. If error, restore from backup                               │
│                                                                  │
│  RULE 3: Path Validation at Every Step                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Validate path:                                                  │
│  • When LLM generates it (Plan mode)                            │
│  • When user approves task                                       │
│  • Immediately before file operation                            │
│                                                                  │
│  RULE 4: No Command Execution (MVP)                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  MVP does NOT execute terminal commands.                        │
│  • No npm install                                                │
│  • No shell commands                                             │
│  • No script execution                                           │
│  Future: Allowlisted commands only with explicit approval.      │
│                                                                  │
│  RULE 5: Size Limits                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Max file size to create: 1MB                                 │
│  • Max files per task: 1                                        │
│  • Max tasks per plan: 50                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Dangerous Operations (Blocked)

```typescript
// BLOCKED_OPERATIONS: Never allow in MVP
const BLOCKED_OPERATIONS = [
  // Shell execution
  'exec',
  'spawn',
  'execSync',
  'spawnSync',
  'system',
  'shell',
  
  // Dangerous commands (for future terminal feature)
  'rm -rf',
  'del /f',
  'format',
  'mkfs',
  'dd',
  ':(){:|:&};:',  // Fork bomb
  
  // Network operations
  'curl',
  'wget',
  'fetch' // (external URLs)
];
```

---

## 5. File Operation Rules

### 5.1 CREATE Operation

```typescript
async function safeCreateFile(
  filePath: string,
  content: string
): Promise<void> {
  // STEP 1: Validate path
  validatePath(filePath);  // Throws if invalid
  
  // STEP 2: Check file doesn't exist
  if (await fileExists(filePath)) {
    throw new Error('File already exists. Use MODIFY instead.');
  }
  
  // STEP 3: Check content size
  if (content.length > MAX_FILE_SIZE) {
    throw new Error(`Content exceeds ${MAX_FILE_SIZE} bytes`);
  }
  
  // STEP 4: Ensure directory exists
  await ensureDirectory(path.dirname(filePath));
  
  // STEP 5: Write file
  await writeFile(filePath, content);
  
  // STEP 6: Log operation
  auditLog('CREATE', filePath, 'success');
}
```

### 5.2 MODIFY Operation

```typescript
async function safeModifyFile(
  filePath: string,
  newContent: string
): Promise<void> {
  // STEP 1: Validate path
  validatePath(filePath);
  
  // STEP 2: Check file exists
  if (!(await fileExists(filePath))) {
    throw new Error('File does not exist. Use CREATE instead.');
  }
  
  // STEP 3: Create backup
  const backupPath = await createBackup(filePath);
  
  try {
    // STEP 4: Write new content
    await writeFile(filePath, newContent);
    
    // STEP 5: Log success
    auditLog('MODIFY', filePath, 'success', { backupPath });
  } catch (error) {
    // STEP 6: Restore on failure
    await restoreFromBackup(backupPath, filePath);
    auditLog('MODIFY', filePath, 'failed_restored', { error });
    throw error;
  }
}
```

### 5.3 DELETE Operation

```typescript
async function safeDeleteFile(filePath: string): Promise<void> {
  // STEP 1: Validate path
  validatePath(filePath);
  
  // STEP 2: Check file exists
  if (!(await fileExists(filePath))) {
    throw new Error('File does not exist');
  }
  
  // STEP 3: Create backup (delete is reversible!)
  const backupPath = await createBackup(filePath);
  
  // STEP 4: Delete file
  await deleteFile(filePath);
  
  // STEP 5: Log operation
  auditLog('DELETE', filePath, 'success', { backupPath });
}
```
---

### 5.4 Backup Cleanup

Backups are automatically cleaned to prevent disk space issues:

```typescript
// Cleanup policy (checked on extension activation)
const BACKUP_POLICY = {
  maxAgeDays: 7,          // Delete backups older than 7 days
  maxTotalSizeMB: 100,    // Delete oldest when total exceeds 100MB
  cleanupOnStartup: true  // Run cleanup on every activation
};
```

Cleanup order:
1. Delete all backups older than maxAgeDays
2. If still over size limit, delete oldest until under limit
3. Never delete backups less than 1 hour old

---

## 6. Validation Functions

### 6.1 Path Validation

```typescript
/**
 * Validates that a path is safe to access.
 * Throws SecurityError if path is invalid or dangerous.
 */
function validatePath(filePath: string): void {
  const workspaceRoot = getWorkspaceRoot();
  
  if (!workspaceRoot) {
    throw new SecurityError('No workspace open');
  }
  
  // Normalize path to absolute
  const absolutePath = path.resolve(workspaceRoot, filePath);
  const normalizedPath = path.normalize(absolutePath);
  
  // CHECK 1: Must be within workspace
  if (!normalizedPath.startsWith(workspaceRoot)) {
    throw new SecurityError(
      `Path "${filePath}" is outside workspace boundary`,
      { filePath, workspaceRoot }
    );
  }
  
  // CHECK 2: No blocked patterns
  for (const pattern of BLOCKED_PATTERNS) {
    if (normalizedPath.toLowerCase().includes(pattern.toLowerCase())) {
      throw new SecurityError(
        `Path contains blocked pattern: ${pattern}`,
        { filePath, pattern }
      );
    }
  }
  
  // CHECK 3: No null bytes (injection prevention)
  if (filePath.includes('\0')) {
    throw new SecurityError('Path contains null byte');
  }
  
  // CHECK 4: Reasonable length
  if (filePath.length > 500) {
    throw new SecurityError('Path too long');
  }
}
```

### 6.2 Content Validation

```typescript
/**
 * Validates content before writing to file.
 */
function validateContent(content: string, filePath: string): void {
  // CHECK 1: Size limit
  const MAX_SIZE = 1024 * 1024; // 1MB
  if (content.length > MAX_SIZE) {
    throw new SecurityError(`Content exceeds ${MAX_SIZE} bytes`);
  }
  
  // CHECK 2: No suspicious patterns in executable files
  const executableExtensions = ['.sh', '.bat', '.cmd', '.ps1'];
  const ext = path.extname(filePath).toLowerCase();
  
  if (executableExtensions.includes(ext)) {
    // Extra scrutiny for scripts
    const dangerousPatterns = ['rm -rf', 'format', ':(){', 'del /f'];
    for (const pattern of dangerousPatterns) {
      if (content.includes(pattern)) {
        throw new SecurityError(
          `Script contains dangerous pattern: ${pattern}`
        );
      }
    }
  }
}
```

---

## 7. Audit & Logging

### 7.1 Audit Log Structure

```typescript
interface AuditEntry {
  timestamp: Date;
  operation: 'CREATE' | 'MODIFY' | 'DELETE' | 'READ';
  filePath: string;
  result: 'success' | 'failed' | 'blocked';
  details?: {
    backupPath?: string;
    error?: string;
    userId?: string;
  };
}

// Log location: {workspace}/.localpilot/audit.log
```

### 7.2 Audit Log Implementation

```typescript
function auditLog(
  operation: string,
  filePath: string,
  result: string,
  details?: Record<string, unknown>
): void {
  const entry = {
    timestamp: new Date().toISOString(),
    operation,
    filePath,
    result,
    details
  };
  
  // Log to output channel
  outputChannel.appendLine(JSON.stringify(entry));
  
  // Log to file (async, don't block)
  appendToAuditFile(entry).catch(console.error);
}
```

---

## 8. Security Checklist

### For Every File Operation

```
┌─────────────────────────────────────────────────────────────────┐
│                  PRE-OPERATION CHECKLIST                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  □ Path validated against workspace root                        │
│  □ Path checked for blocked patterns                            │
│  □ Path normalized (no ../ remaining)                           │
│  □ User has approved this operation                             │
│  □ Backup created (for MODIFY/DELETE)                           │
│  □ Content validated (size, patterns)                           │
│  □ Operation logged to audit                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### For Code Review

```
┌─────────────────────────────────────────────────────────────────┐
│                  SECURITY CODE REVIEW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  □ No direct file system access (use IFileSystem interface)    │
│  □ All paths go through validatePath()                          │
│  □ No shell execution                                            │
│  □ No external network calls                                     │
│  □ User approval required before changes                        │
│  □ Errors don't leak sensitive paths                            │
│  □ Audit logging present                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Document Version: 1.0.0*