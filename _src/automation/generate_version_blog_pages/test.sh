#!/bin/bash

"$meta_executable" --input "test_schangelog.md" --output .

if ! grep -q "Viash 0.0.1" viash-0.0.1/index.qmd ; then
  echo viash-0.0.1/index.qmd should contain "Viash 0.0.1"
  exit 1
fi
if ! grep -q "Viash 0.0.2" viash-0.0.2/index.qmd ; then
  echo viash-0.0.2/index.qmd should contain "Viash 0.0.2"
  exit 1
fi
if grep -q "Viash 0.0.2" viash-0.0.1/index.qmd ; then
  echo viash-0.0.1/index.qmd should not contain "Viash 0.0.2"
  exit 1
fi
if grep -q "Viash 0.0.1" viash-0.0.2/index.qmd ; then
  echo viash-0.0.2/index.qmd should contain "Viash 0.0.1"
  exit 1
fi

if ! grep -q "Summary 1" viash-0.0.1/index.qmd ; then
  echo viash-0.0.1/index.qmd should contain "Viash 0.0.1"
  exit 1
fi
if ! grep -q "Summary 2" viash-0.0.2/index.qmd ; then
  echo viash-0.0.2/index.qmd should contain "Viash 0.0.2"
  exit 1
fi
if grep -q "Summary 2" viash-0.0.1/index.qmd ; then
  echo viash-0.0.1/index.qmd should not contain "Viash 0.0.2"
  exit 1
fi
if grep -q "Summary 1" viash-0.0.2/index.qmd ; then
  echo viash-0.0.2/index.qmd should contain "Viash 0.0.1"
  exit 1
fi