#!/usr/bin/env node
import fs from 'node:fs/promises';
import { createWriteStream } from 'node:fs';
import path from 'node:path';
// Optional dependency handling
let ignoreModule = null;
try {
  // Dynamic import for the ignore package
  ignoreModule = await import('ignore').then(m => m.default);
} catch (error) {
  console.warn('Warning: "ignore" package not installed. .gitignore support disabled.');
}

// --- Default Configuration (and other functions like parseArgs, walk, langForExt, etc.) ---
const DEFAULT_ROOTS = ['.'];
const DEFAULT_EXCLUDE_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', 'out', 'target', 'vendor',
  '.idea', '.vscode', '.DS_Store', 'coverage', '.cache', 'bin', 'obj',
  '.venv', '__pycache__', '.tox',
  'Pods', 'DerivedData', '.swiftpm', 'Carthage',
  '.gradle',
  'Library', 'Temp', 'Logs', 'Packages',
  'Intermediate', 'Saved',
]);
const DEFAULT_ALLOW_EXTS = new Set([
  '.ts', '.tsx', '.js', '.jsx', '.json', '.mjs', '.cjs', '.html', '.css', '.scss', '.less',
  '.yml', '.yaml', '.toml', '.ini', '.env', '.config',
  '.md', '.mdx', '.txt','csv','.json',
  '.sh', '.bash', '.ps1', 'Dockerfile',
  '.c', '.cpp', '.h', '.hpp',
  '.py', '.go', '.rs', '.rb', '.php', '.sql',
  '.cs', '.gd', '.lua', '.glsl', '.hlsl', '.metal', '.shader', '.tscn', '.tres',
  '.swift', '.m', '.storyboard', '.xib', '.plist', 'Podfile',
  '.kt', '.kts', '.java', '.xml', '.gradle', '.gradle.kts',
  '.dart', '.xaml',
]);
const DEFAULT_EXCLUDE_FILE_BASENAMES = new Set([
  'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock', 'Podfile.lock', 'Cargo.lock',
  'composer.lock', 'Gemfile.lock' , 'reviewer.md'
]);
const langForExt = (ext) => ({
  '.ts': 'typescript', '.tsx': 'tsx', '.js': 'javascript', '.jsx': 'jsx', '.mjs': 'javascript', '.cjs': 'javascript',
  '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml', '.toml':'toml', '.ini':'ini',
  '.md': 'markdown', '.mdx': 'mdx', '.txt': 'text',
  '.sh': 'bash', '.bash': 'bash', '.ps1': 'powershell', 'Dockerfile':'dockerfile',
  '.py': 'python', '.go': 'go', '.rs': 'rust',
  '.java': 'java', '.kt': 'kotlin', '.kts': 'kotlin', '.scala': 'scala', '.gradle': 'groovy', '.gradle.kts': 'kotlin',
  '.cs': 'csharp', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
  '.rb': 'ruby', 'Podfile': 'ruby', '.php': 'php', '.sql': 'sql',
  '.html': 'html', '.css': 'css', '.scss': 'scss', '.less': 'less',
  '.gd': 'gdscript', '.lua': 'lua', '.glsl': 'glsl', '.hlsl': 'hlsl', '.metal': 'c++', '.shader': 'csharp', '.tscn': 'ini', '.tres': 'ini',
  '.swift': 'swift', '.m': 'objectivec',
  '.xml': 'xml', '.storyboard': 'xml', '.xib': 'xml', '.plist': 'xml', '.xaml': 'xml',
  '.dart': 'dart',
}[ext] || '');

function parseArgs(argv) {
  const config = {
    roots: [], out: '', maxBytes: 524288, help: false,
    excludeDirs: new Set(DEFAULT_EXCLUDE_DIRS),
    useGitignore: true,
    allowExts: new Set(DEFAULT_ALLOW_EXTS),
    excludeFiles: new Set(DEFAULT_EXCLUDE_FILE_BASENAMES),
  };
  const parseList = (arg, prefix) => arg.slice(prefix.length).split(',').filter(Boolean);
  for (const arg of argv) {
    if (arg === '-h' || arg === '--help') { config.help = true; continue; }
    if (arg.startsWith('--out=')) { config.out = arg.slice('--out='.length); continue; }
    if (arg === '--no-gitignore') { config.useGitignore = false; continue; }
    if (arg.startsWith('--max-bytes=')) {
      const n = Number(arg.slice('--max-bytes='.length));
      if (Number.isFinite(n) && n >= 0) config.maxBytes = Math.trunc(n);
      continue;
    }
    if (arg.startsWith('--exclude-dir=')) { parseList(arg, '--exclude-dir=').forEach(d => config.excludeDirs.add(d)); continue; }
    if (arg.startsWith('--include-ext=')) {
      if (config.allowExts === DEFAULT_ALLOW_EXTS) config.allowExts = new Set();
      parseList(arg, '--include-ext=').forEach(e => config.allowExts.add(e.startsWith('.') ? e : `.${e}`));
      continue;
    }
    if (arg.startsWith('--exclude-file=')) { parseList(arg, '--exclude-file=').forEach(f => config.excludeFiles.add(f)); continue; }
    if (!arg.startsWith('--')) { config.roots.push(arg); }
  }
  if (config.roots.length === 0) { config.roots = DEFAULT_ROOTS; }
  return config;
}

/**
 * Load and parse .gitignore file for a given directory
 * @param {string} rootDir - The directory containing the .gitignore file
 * @returns {object|null} An ignore instance that can be used to test paths, or null if not available
 */
async function loadGitignore(rootDir) {
  if (!ignoreModule) return null;
  
  const ig = ignoreModule();
  try {
    const content = await fs.readFile(path.join(rootDir, '.gitignore'), 'utf8');
    ig.add(content);
  } catch {
    // No .gitignore found or couldn't read it
  }
  return ig;
}

async function walk(dir, allowExts, excludeDirs, gitignore = null, rootDir = '', files = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const absPath = path.join(dir, entry.name);
      const relPath = rootDir ? path.relative(rootDir, absPath) : absPath;
      
      // Check gitignore if available
      if (gitignore && gitignore.ignores(relPath.split(path.sep).join('/'))) {
        continue;
      }
      
      if (entry.isDirectory()) {
        if (!excludeDirs.has(entry.name)) {
          await walk(absPath, allowExts, excludeDirs, gitignore, rootDir, files);
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name);
        if (allowExts.has(ext) || allowExts.has(entry.name)) {
          files.push(absPath);
        }
      }
    }
  } catch (error) {
    console.warn(`Warning: Could not read directory "${dir}": ${error.message}`);
  }
  return files;
}

async function isTextFile(filePath) {
  try {
    const fd = await fs.open(filePath, 'r');
    const buffer = Buffer.alloc(4096);
    const { bytesRead } = await fd.read(buffer, 0, 4096, 0);
    await fd.close();
    
    // Check for NULL bytes which indicate binary content
    for (let i = 0; i < bytesRead; i++) {
      if (buffer[i] === 0) return false;
    }
    return true;
  } catch {
    return false;
  }
}

/**
 * Generates a table of contents for easier navigation
 * @param {Array} fileEntries - Array of file entry objects
 * @returns {string} Markdown formatted table of contents
 */
function generateTableOfContents(fileEntries) {
  let toc = "## Table of Contents\n\n";
  fileEntries.forEach(({ rel }) => {
    // Create markdown heading link using the file path
    const linkText = rel.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
    toc += `- [${rel}](#${linkText})\n`;
  });
  return toc + "\n\n---\n\n";
}

/**
 * Generates a visually appealing and informative text-based tree structure.
 * - Directories are marked with a trailing '/'
 * - Entries are sorted with directories first, then files, all alphabetically.
 * - Provides a header with the root name and total file count.
 * @param {string[]} files - An array of relative file paths (using '/' as separator).
 * @param {string} rootDisplayName - The name to display for the root of the tree.
 * @returns {string} The formatted tree string.
 */
function generateTree(files, rootDisplayName = '.') {
    const tree = {};

    for (const file of files) {
        // *** THE FIX IS HERE: Using '/' explicitly ***
        const parts = file.split('/'); 
        let currentLevel = tree;
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const isLast = i === parts.length - 1;

            if (!currentLevel[part]) {
                currentLevel[part] = {
                    type: isLast ? 'file' : 'directory',
                    children: isLast ? null : {},
                };
            }
            currentLevel = currentLevel[part].children;
        }
    }

    const buildTreeString = (node, prefix = '') => {
        let result = '';
        const entries = Object.entries(node).sort(([aName, aNode], [bName, bNode]) => {
            if (aNode.type === bNode.type) {
                return aName.localeCompare(bName);
            }
            return aNode.type === 'directory' ? -1 : 1;
        });

        entries.forEach(([name, childNode], index) => {
            const isLast = index === entries.length - 1;
            const connector = isLast ? '└── ' : '├── ';
            const displayName = childNode.type === 'directory' ? `${name}/` : name;
            
            result += `${prefix}${connector}${displayName}\n`;

            if (childNode.children) {
                const childPrefix = prefix + (isLast ? '    ' : '│   ');
                result += buildTreeString(childNode.children, childPrefix);
            }
        });
        return result;
    };

    const fileCount = files.length === 1 ? '1 file' : `${files.length} files`;
    const header = `${rootDisplayName} (${fileCount})\n`;
    return header + buildTreeString(tree);
}

async function main() {
  const config = parseArgs(process.argv.slice(2));

  if (config.help) {
    console.log(`
Usage: export-to-mdnew.mjs [options] [directories...]

Options:
  --out=FILE               Output file path (default: docs/code-snapshot.md)
  --max-bytes=N            Skip files larger than N bytes (default: 524288)
  --exclude-dir=A,B,C      Exclude directories (comma-separated)
  --include-ext=.a,.b,.c   Include only files with these extensions
  --exclude-file=A,B,C     Exclude files by name (comma-separated)
  --no-gitignore           Don't respect .gitignore files
  -h, --help               Show this help message
`);
    return;
  }

  const roots = config.roots.map((p) => path.resolve(p));
  const allFiles = [];
  
  // Load gitignore for each root if enabled and module is available
  const gitignores = {};
  if (config.useGitignore && ignoreModule) {
    for (const root of roots) {
      gitignores[root] = await loadGitignore(root);
    }
  } else if (config.useGitignore) {
    console.warn('Warning: .gitignore support is disabled because the "ignore" package is not installed.');
  }
  
  for (const r of roots) {
    const stat = await fs.stat(r).catch(() => null);
    if (stat?.isDirectory()) {
      const gitignore = config.useGitignore ? gitignores[r] : null;
      await walk(r, config.allowExts, config.excludeDirs, gitignore, r, allFiles);
    }
  }

  const filePairs = allFiles.map((abs) => {
    // This part correctly normalizes paths to use '/'
    const rel = path.relative(process.cwd(), abs).split(path.sep).join('/');
    return { abs, rel };
  }).sort((a, b) => a.rel.localeCompare(b.rel));
  
  const rootDisplayNames = roots.map(r => path.relative(process.cwd(), r) || '.').join(', ');
  const tree = generateTree(filePairs.map(p => p.rel), rootDisplayNames);
  
  const header = `# Code Snapshot

**Generated:** ${new Date().toISOString()}
**Roots:** ${rootDisplayNames}
**Max file size:** ${config.maxBytes === 0 ? 'unlimited' : config.maxBytes.toLocaleString() + ' bytes'}

## Project Structure

\`\`\`
${tree}
\`\`\`

---
`;
  
  const fenceFor = (content) => content.includes('```') ? '````' : '```';
  
  let skippedLarge = 0;
  let skippedNamed = 0;
  let skippedBinary = 0;
  let included = 0;
  const fileEntries = [];
  
  // Add progress indicator
  const totalFiles = filePairs.length;
  console.log(`Processing ${totalFiles} files...`);
  let processedCount = 0;
  
  for (const { abs, rel } of filePairs) {
    // Update progress
    processedCount++;
    if (processedCount % 10 === 0 || processedCount === totalFiles) {
      process.stdout.write(`\rProcessing: ${processedCount}/${totalFiles} (${Math.round(processedCount/totalFiles*100)}%)`);
    }
   
    const base = path.basename(abs);
   
    if (config.excludeFiles.has(base)) { 
      skippedNamed++; 
      continue; 
    }
   
    // Check if it's a binary file
    if (!(await isTextFile(abs))) {
      skippedBinary++;
      continue;
    }
   
    if (config.maxBytes > 0) {
      try {
        const stats = await fs.stat(abs);
        if (stats.size > config.maxBytes) {
          skippedLarge++;
          continue;
        }
      } catch {
        continue;
      }
    }
    
    try {
      const content = await fs.readFile(abs, 'utf8');
      included++;
      const lang = langForExt(path.extname(abs) || path.basename(abs));
      const fence = fenceFor(content);
      const stats = await fs.stat(abs);
      fileEntries.push({ 
        rel, 
        lang, 
        fence, 
        content,
        size: stats.size,
        modified: stats.mtime.toISOString()
      });
    } catch {
      // Skip files we can't read
    }
  }

  console.log('\nGenerating markdown output...');
  const target = path.resolve(config.out || 'docs/code-snapshot.md');
  await fs.mkdir(path.dirname(target), { recursive: true });
  
  // Use stream for better performance with large files
  const writeStream = createWriteStream(target);
  writeStream.write(header);
  
  // Add table of contents
  writeStream.write(generateTableOfContents(fileEntries));
  
  for (const { rel, lang, fence, content, size, modified } of fileEntries) {
    // Write the file section with collapsible details tag
    writeStream.write(`## ${rel}\n\n`);
    writeStream.write(`*Size: ${size.toLocaleString()} bytes | Modified: ${modified}*\n\n`);
    writeStream.write(`<details>\n<summary>View code</summary>\n\n`);
    writeStream.write(`${fence}${lang}\n${content}\n${fence}\n\n`);
    writeStream.write(`</details>\n\n\n`);
  }
  
  // Close the stream
  writeStream.end();
  
  // Wait for the write to complete
  await new Promise((resolve) => writeStream.on('finish', resolve));
  
  const summaryParts = [`${included} files included`]; 
  if (skippedLarge > 0) summaryParts.push(`${skippedLarge} skipped (> ${config.maxBytes.toLocaleString()} bytes)`);
  if (skippedNamed > 0) summaryParts.push(`${skippedNamed} skipped by name`);
  if (skippedBinary > 0) summaryParts.push(`${skippedBinary} skipped (binary files)`);

  console.log(`Wrote to ${target} (${summaryParts.join(', ')})`);
}

// This is the entry point of the script
(async function() {
  try {
    await main();
  } catch (e) {
    console.error('An unexpected error occurred:', e);
    process.exit(1);
  }
})();