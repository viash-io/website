const fs = require('fs');

// VIASH START
let par = {
  'input': 'path/to/file.txt',
  'output': 'output.txt'
};
// VIASH END

// copy file
console.log(`Copying '${par['input']}' to '${par['output']}'`)
fs.copyFile(par['input'], par['output'], (err) => {
  if (err) throw err;
});

