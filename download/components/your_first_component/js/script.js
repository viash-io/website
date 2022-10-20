const fs = require('fs');

console.log(`Copying '${par['input']}' to '${par['output']}'`)
fs.copyFile(par['input'], par['output'], (err) => {
  if (err) throw err;
});