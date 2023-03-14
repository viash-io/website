import shutil

## VIASH START
par = {
  'input': 'file.txt',
  'output': 'output.txt'
}
## VIASH END

# copy file
print(f"Copying '{par['input']}' to '{par['output']}'.")
shutil.copyfile(par['input'], par['output'])
