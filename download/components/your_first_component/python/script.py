import shutil

print(f"Copying '{par['input']}' to '{par['output']}'.")
shutil.copyfile(par['input'], par['output'])