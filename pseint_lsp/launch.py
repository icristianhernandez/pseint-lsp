#!/usr/bin/env python3
"""
PSeInt LSP Server launcher
This script resolves path issues and ensures the server runs correctly
"""
import os
import sys
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent.absolute()
server_path = script_dir / "server.py"

# Add the script directory to Python path for imports
sys.path.insert(0, str(script_dir))

# Import and run the server
def main():
    # Change to the script directory to ensure relative imports work
    os.chdir(script_dir)
    
    # Import the server module
    import server
    
    # Run the server
    server.run()

if __name__ == "__main__":
    main()
