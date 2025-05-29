#!/usr/bin/env bash
set -o errexit
echo "Current directory: $(pwd)"
echo "Listing files: $(ls -la)"
pip install -r requirements.txt
mkdir -p instance