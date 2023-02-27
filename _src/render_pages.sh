#!/bin/bash

viash run _src/automation/generate_version_blog_pages/config.vsh.yaml -- \
  --input ../viash/CHANGELOG.md \
  --output blog/posts

python _src/automation/generate_cli_schema_export_pages.py

python _src/automation/generate_config_schema_export_pages.py
