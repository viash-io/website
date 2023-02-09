const fs = require('fs');
const child_process = require('child_process');

// VIASH START
let meta = {
  'executable': 'target/example_js'
};
// VIASH END

const inputPath = 'foo.txt';
const outputPath = 'bar.txt';
const content = 'hello\nthere\n';

console.log('>>> Create input test file');
fs.writeFileSync(inputPath, content, 'utf8');

console.log('>>> Run executable');
const cmdArgs = [
  '--input', inputPath,
  '--output', outputPath
];
const child = child_process.spawnSync(meta["executable"], cmdArgs);
if (child.error) {
  console.error(`Error: ${child.error}`);
  process.exit(1);
}

console.log('>>> Check whether output file exists');
if (!fs.existsSync(outputPath)) {
  console.error('Output file was not found');
  process.exit(1);
}

console.log('>>> Check whether input and output file are the same');
const outputLines = fs.readFileSync(outputPath, 'utf8');
if (content !== outputLines) {
  console.error(
    `Input and output should be the same\n` +
    `expected content: ${content}\n` +
    `found: ${outputLines}\n`
  );
  process.exit(1);
}

console.log('>>> Test finished successfully');