#!/usr/bin/env bash
# Exit immediately if a pipeline, which may consist of a single simple command, exits with a non-zero status
set -o errexit

echo "--- Upgrading pip and installing project dependencies ---"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "--- Render build script completed successfully ---"
