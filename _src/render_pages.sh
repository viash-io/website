#!/bin/bash


echo "Creating blog posts"
viash run _src/automation/generate_version_blog_pages/config.vsh.yaml -- \
  --input ../viash/CHANGELOG.md \
  --output blog/posts

source renv/python/virtualenvs/renv-python-3.10/bin/activate

echo "Creating cli information"
python _src/automation/generate_cli_schema_export_pages.py

echo "Creating config information"
python _src/automation/generate_config_schema_export_pages.py
