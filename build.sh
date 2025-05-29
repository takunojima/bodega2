#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Current directory: $(pwd)"
echo "Listing files: $(ls -la)"

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories if they don't exist
mkdir -p instance 