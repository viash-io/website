#!/bin/bash


echo "Creating blog posts"
viash run _src/automation/generate_version_blog_pages/config.vsh.yaml -- \
  --input ../viash/CHANGELOG.md \
  --output blog/posts

echo "Creating cli information"
viash export cli_schema --output ./reference/cli_schema_export.json
viash run _src/automation/generate_reference_cli_pages/config.vsh.yaml -- \
  --input ./reference/cli_schema_export.json

echo "Creating config information"
viash export config_schema --output ./reference/config_schema_export.json
viash run _src/automation/generate_reference_config_pages/config.vsh.yaml -- \
  --input ./reference/config_schema_export.json
