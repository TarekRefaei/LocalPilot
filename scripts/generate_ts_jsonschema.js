/**
 * Generate JSON Schemas for TypeScript contract interfaces using ts-json-schema-generator.
 *
 * Usage:
 *   node scripts/generate_ts_jsonschema.js <ts-file> <typeName> <out.json>
 */
const path = require('path');
const fs = require('fs');
const { createGenerator } = require('ts-json-schema-generator');

function gen(tsFile, typeName, outFile) {
  const config = {
    path: tsFile,
    tsconfig: path.join(process.cwd(), 'tsconfig.json'),
    type: typeName,
    expose: 'all',
    topRef: true,
    skipTypeCheck: false,
  };
  const generator = createGenerator(config);
  const schema = generator.createSchema(config.type);
  fs.writeFileSync(outFile, JSON.stringify(schema, null, 2), 'utf-8');
  console.log('Wrote', outFile);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error('Usage: node scripts/generate_ts_jsonschema.js file.ts TypeName out.json');
    process.exit(2);
  }
  gen(args[0], args[1], args[2]);
}
