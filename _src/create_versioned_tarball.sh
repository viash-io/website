#!/bin/bash

# Create a tar.xz archive of _site, excluding versions.js and versions.json,
# and store it as _versioned/<version>.tar.xz with contents in a <version>/ folder.
# Usage: ./create_versioned_tarball.sh <version>

if [ -z "$1" ]; then
  echo "Error: Version argument required"
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION="$1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

SITE_DIR="$REPO_ROOT/_site"
OUTPUT="$REPO_ROOT/_versioned/${VERSION}.tar.xz"

mkdir -p "$(dirname "$OUTPUT")"

tar \
  --create \
  --xz \
  --file "$OUTPUT" \
  --exclude="versions.js" \
  --exclude="versions.json" \
  --exclude="_versioned" \
  --transform "s|^\\.|${VERSION}|" \
  --directory "$SITE_DIR" \
  .

echo "Created $OUTPUT with contents in ${VERSION}/ folder"
