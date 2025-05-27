#!/bin/bash
# PSeInt LSP Server launcher script
# This script ensures the correct path is used to run the server

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the Python server with the absolute path
exec python3 -m src.server "$@"
