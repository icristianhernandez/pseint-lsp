#!/usr/bin/env python3
"""
Setup script for PSeInt LSP Server
This script provides the correct paths and configuration for LSP clients
"""
from pathlib import Path

def get_server_info():
    """Get server path and configuration information"""
    script_dir = Path(__file__).parent.absolute()
    server_path = script_dir / "server.py"
    launch_path = script_dir / "launch.py"
    
    print("PSeInt LSP Server Configuration")
    print("=" * 40)
    print(f"Server directory: {script_dir}")
    print(f"Main server file: {server_path}")
    print(f"Launcher script: {launch_path}")
    print()
    print("Recommended LSP client command:")
    print(f"python3 {launch_path}")
    print()
    print("Alternative command:")
    print(f"python3 {server_path}")
    print()
    print("Make sure your LSP client uses the absolute path above.")
    print("Do NOT use paths with ~ (tilde) as they may not expand correctly.")

if __name__ == "__main__":
    get_server_info()
