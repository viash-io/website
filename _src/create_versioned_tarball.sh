#!/bin/bash

# Create a tar.xz archive of _site, excluding versions.js and versions.json,
# and store it as _versioned/new.tar.xz.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

SITE_DIR="$REPO_ROOT/_site"
OUTPUT="$REPO_ROOT/_versioned/new.tar.xz"

mkdir -p "$(dirname "$OUTPUT")"

tar \
  --create \
  --xz \
  --file "$OUTPUT" \
  --exclude="versions.js" \
  --exclude="versions.json" \
  --exclude="_versioned" \
  --directory "$SITE_DIR" \
  .

echo "Created $OUTPUT"
