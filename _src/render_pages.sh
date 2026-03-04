#!/bin/bash

source renv/python/virtualenvs/renv-python-3.13/bin/activate
export PYTHONPATH="$(pwd)/renv/python/virtualenvs/renv-python-3.13/lib/python3.13/site-packages:${PYTHONPATH}"

echo "Creating blog posts"
viash run _src/automation/generate_version_blog_pages/config.vsh.yaml -- \
  --input ../viash/CHANGELOG.md \
  --output blog/posts

echo "Removing reference subfolders but leaving top level files in place"
rm -rf ./reference/*/

echo "Copying static reference pages"
cp -r ../viash/docs/reference/* ./reference

echo "Creating cli information"
viash export cli_schema --output ./reference/cli_schema_export.json --format json
viash run _src/automation/generate_reference_cli_pages/config.vsh.yaml -- \
  --input ./reference/cli_schema_export.json

echo "Creating config information"
viash export config_schema --output ./reference/config_schema_export.json --format json
viash run _src/automation/generate_reference_config_pages/config.vsh.yaml -- \
  --input ./reference/config_schema_export.json

echo "Creating reference main page"
viash run ./_src/automation/generate_reference_main_index_page/config.vsh.yaml