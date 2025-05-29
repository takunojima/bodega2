#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies and build frontend
npm install
npm run build

# Create database directory if it doesn't exist
mkdir -p instance

# Initialize database
python init_db.py 