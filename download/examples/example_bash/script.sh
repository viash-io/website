#!/bin/bash

## VIASH START
par_input=path/to/file.txt
par_output=output.txt
## VIASH END

echo "Copying '$par_input' to '$par_output'."
cp -r "$par_input" "$par_output"