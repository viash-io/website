import subprocess
import os

input_path = "foo.txt"
output_path = "bar.txt"
content = "hello\nthere\n"

## VIASH START
meta = {
  "executable" = "target/example_python"
}
## VIASH END

print(">>> Create input test file")
with open(input_path, "w") as file:
  file.write(content)

print(">>> Run executable")
cmd_args = [
  meta["executable"],
  "--input", input_path,
  "--output", output_path
]
subprocess.run(cmd_args, check=True)

print(">>> Check whether output file exists")
assert os.path.exists(output_path), "Output file was not found"

print(">>> Check whether input and output file are the same")
with open(output_path, "r", encoding="utf8") as file:
  output_lines = file.read()

assert content == output_lines, \
  "Input and output should be the same" \
  f"expected content: {content}" \
  f"found: {output_lines}"

print(">>> Test finished successfully")