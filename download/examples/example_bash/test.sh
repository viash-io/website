#!/bin/bash

echo ">>> Create input test file"
echo "foo" > foo.txt

echo ">>> Run executable"
$meta_executable --input foo.txt --output bar.txt

echo ">>> Check whether output file exists"
[[ -f bar.txt ]] || (echo "Output file could not be found!" && exit 1)

echo ">>> Check whether input and output file are the same"
cmp foo.txt bar.txt || (echo "Input and output files are different!" && exit 1)

echo ">>> Test finished successfully"
