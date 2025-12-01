// scripts/generate_all_ts_jsonschemas.js
// Generate JSON Schemas for all exported interfaces in extension/src/contracts/*.ts
const fs = require('fs');
const path = require('path');
const { createGenerator } = require('ts-json-schema-generator');

function findContracts(rootDir) {
  const files = [];
  const entries = fs.readdirSync(rootDir, { withFileTypes: true });
  for (const ent of entries) {
    if (ent.isFile() && ent.name.endsWith('.ts')) files.push(path.join(rootDir, ent.name));
  }
  return files;
}

function extractInterfaces(tsFile) {
  const src = fs.readFileSync(tsFile, 'utf8');
  const re = /export\s+interface\s+([A-Za-z0-9_]+)/g;
  const out = [];
  let m;
  while ((m = re.exec(src)) !== null) {
    out.push(m[1]);
  }
  return out;
}

function main() {
  const repoRoot = path.resolve(__dirname, '..');
  const contractsDir = path.join(repoRoot, 'extension', 'src', 'contracts');
  const outDir = path.join(repoRoot, 'schemas_ts');
  if (!fs.existsSync(contractsDir)) {
    console.error('Contracts directory not found:', contractsDir);
    process.exit(2);
  }
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const files = findContracts(contractsDir);
  if (files.length === 0) {
    console.warn('No contract .ts files found in', contractsDir);
  }

  let count = 0;
  for (const file of files) {
    const types = extractInterfaces(file);
    for (const typeName of types) {
      const config = {
        path: file,
        tsconfig: path.join(repoRoot, 'extension', 'tsconfig.json'),
        type: typeName,
        topRef: true,
        expose: 'export',
        skipTypeCheck: false,
      };
      try {
        const generator = createGenerator(config);
        const schema = generator.createSchema(config.type);
        const outFile = path.join(outDir, `${typeName}.json`);
        fs.writeFileSync(outFile, JSON.stringify(schema, null, 2));
        console.log('Wrote', outFile);
        count++;
      } catch (e) {
        console.warn(`Failed to generate schema for ${typeName} in ${path.basename(file)}:`, e.message || e);
      }
    }
  }
  console.log(`Completed. Generated ${count} schema files.`);
}

if (require.main === module) {
  main();
}
