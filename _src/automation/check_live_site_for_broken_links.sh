#!/usr/bin/env bash

# Uses https://www.npmjs.com/package/broken-link-checker-local

if ! command -v blcl &> /dev/null
then
    echo "blcl could not be found, attempting to install..."
	npm install -g broken-link-checker-local
fi

blcl https://viash.io/ -ro