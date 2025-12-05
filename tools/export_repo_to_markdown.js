#!/usr/bin/env node
/**
 * export_repo_to_markdown.js
 *
 * Usage:
 *   node tools/export_repo_to_markdown.js /path/to/repo output.md
 *
 * Example (from repo root):
 *   node tools/export_repo_to_markdown.js . repo_export.md
 *
 * Output: repo_export.md with:
 *  - Project information header
 *  - ASCII tree of files (excluding ignored patterns)
 *  - Each text file included as fenced code block with file path header
 *
 * Configurable: adjust IGNORES and MAX_FILE_SIZE_BYTES below.
 */

const fs = require('fs').promises;
const path = require('path');

const IGNORES = [
  'node_modules',
  '.git',
  '.venv',
  'venv',
  '__pycache__',
  'dist',
  'build',
  '.next',
  'out',
  '.gradle',
  'Pods',
  'DerivedData',
  '*.lock',
];

const DEFAULT_MAX_FILE_SIZE_BYTES = 200 * 1024; // 200 KB - skip huge files to keep markdown sane

function matchesIgnore(filePath) {
  const parts = filePath.split(path.sep);
  for (const p of parts) {
    for (const ig of IGNORES) {
      // simple wildcard: '*.lock'
      if (ig.startsWith('*')) {
        if (p.endsWith(ig.slice(1))) return true;
      } else if (ig.includes('*')) {
        // not a complex glob implementation; skip
        continue;
      } else if (p === ig) return true;
    }
  }
  return false;
}

async function isBinaryFile(fullPath) {
  try {
    const fd = await fs.open(fullPath, 'r');
    const { buffer } = await fd.read(Buffer.alloc(1024), 0, 1024, 0);
    await fd.close();
    // If any null byte -> binary
    for (let i = 0; i < buffer.length; i++) {
      if (buffer[i] === 0) return true;
    }
    return false;
  } catch (e) {
    return true;
  }
}

async function walk(dir, baseDir) {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch (e) {
    return [];
  }
  const results = [];
  for (const ent of entries) {
    const rel = path.relative(baseDir, path.join(dir, ent.name));
    if (matchesIgnore(rel)) continue;
    if (ent.isDirectory()) {
      results.push({ path: rel, type: 'dir' });
      const children = await walk(path.join(dir, ent.name), baseDir);
      for (const c of children) results.push(c);
    } else if (ent.isFile()) {
      results.push({ path: rel, type: 'file' });
    } else {
      // skip symlinks and others
    }
  }
  return results;
}

function makeTreeMarkdown(fileList) {
  // Build nested structure
  const tree = {};
  for (const item of fileList) {
    const parts = item.path.split(path.sep);
    let cur = tree;
    for (let i = 0; i < parts.length; i++) {
      const p = parts[i];
      if (!cur[p]) cur[p] = { __meta: null };
      if (i === parts.length - 1) {
        cur[p].__meta = { type: item.type, path: item.path };
      } else {
        if (!cur[p].__children) cur[p].__children = {};
        cur = cur[p].__children;
      }
    }
  }

  function render(node, prefix = '') {
    const keys = Object.keys(node);
    // sort directories before files
    keys.sort((a, b) => {
      if (a === '__meta') return 1;
      if (b === '__meta') return -1;
      const na = node[a].__meta ? 1 : 0;
      const nb = node[b].__meta ? 1 : 0;
      // directories (no __meta) should come first
      return nb - na || a.localeCompare(b);
    });

    const lines = [];
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i];
      if (k === '__meta') continue;
      const child = node[k];
      const isLast = i === keys.length - 1;
      const pointer = isLast ? '└─' : '├─';
      const meta = child.__meta;
      if (meta && meta.type === 'dir') {
        lines.push(`${prefix}${pointer} ${k}/`);
        if (child.__children) {
          const more = render(child.__children, prefix + (isLast ? '   ' : '│  '));
          lines.push(...more);
        }
      } else if (meta && meta.type === 'file') {
        lines.push(`${prefix}${pointer} ${k}`);
      } else if (child.__children) {
        lines.push(`${prefix}${pointer} ${k}/`);
        const more = render(child.__children, prefix + (isLast ? '   ' : '│  '));
        lines.push(...more);
      } else {
        lines.push(`${prefix}${pointer} ${k}`);
      }
    }
    return lines;
  }

  const mdLines = ['```text', ...render(tree), '```', ''];
  return mdLines.join('\n');
}

function safeFence(content) {
  // Replace any ``` with ```\u200b to avoid closing fences inside content
  return content.replace(/```/g, '```​');
}

async function exportToMarkdown(rootDir, outFile, maxFileSizeBytes = DEFAULT_MAX_FILE_SIZE_BYTES) {
  const absRoot = path.resolve(rootDir);
  const items = await walk(absRoot, absRoot);

  // Compose header
  const header = [
    `# Repository export: ${path.basename(absRoot)}`,
    '',
    `**Path:** ${absRoot}`,
    '',
    `**Generated:** ${new Date().toISOString()}`,
    '',
    '## Project tree',
    '',
  ].join('\n');

  const treeMd = makeTreeMarkdown(items);

  let md = header + treeMd + '\n\n';
  md += '---\n\n';
  md += '## Files content\n\n';

  // For each file include contents
  for (const item of items) {
    if (item.type !== 'file') continue;
    const fullPath = path.join(absRoot, item.path);
    let stat;
    try {
      stat = await fs.stat(fullPath);
    } catch (e) {
      continue;
    }
    if (stat.size > maxFileSizeBytes) {
      md += `### ${item.path}\n\n`;
      md += `> Skipped: file size ${stat.size} bytes > ${maxFileSizeBytes} bytes (configure MAX_FILE_SIZE_BYTES to include large files)\n\n`;
      continue;
    }
    const binary = await isBinaryFile(fullPath);
    if (binary) {
      md += `### ${item.path}\n\n`;
      md += `> Skipped binary file\n\n`;
      continue;
    }
    let content;
    try {
      content = await fs.readFile(fullPath, 'utf-8');
    } catch (e) {
      md += `### ${item.path}\n\n`;
      md += `> Failed to read file: ${String(e)}\n\n`;
      continue;
    }
    md += `### ${item.path}\n\n`;
    md += '```' + '\n';
    md += safeFence(content) + '\n';
    md += '```\n\n';
  }

  await fs.writeFile(outFile, md, 'utf-8');
  console.log(`Export complete: ${outFile}`);
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node tools/export_repo_to_markdown.js <repoRoot> <outMarkdownFile> [maxFileSizeBytes]');
    process.exit(2);
  }
  const repoRoot = args[0];
  const outFile = args[1];
  const maxFileSize = args[2] ? parseInt(args[2], 10) : DEFAULT_MAX_FILE_SIZE_BYTES;
  await exportToMarkdown(repoRoot, outFile, maxFileSize);
}

if (require.main === module) main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
