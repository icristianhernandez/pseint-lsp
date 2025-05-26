#!/bin/bash
# Enhanced setup script for PSeInt LSP development environment with Ruff and Pyright

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and essential development tools
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    git \
    build-essential \
    curl \
    wget \
    make \
    gcc \
    g++ \
    libc6-dev \
    libffi-dev \
    libssl-dev

# Install Node.js for Pyright (using NodeSource repository for latest LTS)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Install additional development tools
sudo apt install -y \
    vim \
    nano \
    tree \
    htop \
    jq \
    unzip

cd /app

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip to latest version
python -m pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install Pyright globally via npm
sudo npm install -g pyright

# Make scripts executable
chmod +x run_server.sh
chmod +x tests/run_all_tests.py

# Set up pre-commit hooks (optional)
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "Pre-commit hooks installed"
fi

# Run initial linting and formatting
echo "Running Ruff formatting and linting..."
ruff format .
ruff check --fix . || true

# Run type checking
echo "Running Pyright type checking..."
pyright . || true

# Run initial tests to verify setup
echo "Running initial tests..."
python -m pytest tests/ -v

# Display installed packages
echo "Installed Python packages:"
pip list

echo ""
echo "=== Setup complete! ==="
echo "Virtual environment is activated."
echo ""
echo "Available commands:"
echo "  make help     - Show all available make targets"
echo "  make test     - Run tests"
echo "  make lint     - Run linting (ruff + pyright)"
echo "  make format   - Format code with ruff"
echo "  make check    - Run format and lint checks"
echo "  ./run_server.sh - Run the LSP server"
echo ""
echo "Tools installed:"
echo "  - Ruff (linting + formatting): $(ruff --version)"
echo "  - Pyright (type checking): $(pyright --version)"
echo "  - Python: $(python --version)"
echo "  - Node.js: $(node --version)"
