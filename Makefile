# Makefile for PSeInt LSP development
# This demonstrates how Make is commonly used in Python projects

# Configuration
PYTHON := python3
PIP := pip
VENV_DIR := .venv
SRC_DIRS := . tests/

.PHONY: help install install-dev test lint format clean setup check dev run watch

# Default target - shows help
help:
	@echo "PSeInt LSP Development Commands (using Ruff + Pyright)"
	@echo "========================================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup       - Set up development environment"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  dev         - Start development mode (install deps + run server)"
	@echo "  run         - Run the LSP server"
	@echo "  server      - Alias for run"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  lint        - Run linting and type checking (ruff + pyright)"
	@echo "  format      - Format code with ruff"
	@echo "  check       - Run both linting and formatting checks (CI mode)"
	@echo "  fix         - Auto-fix code issues where possible"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test        - Run all tests"
	@echo "  test-cov    - Run tests with coverage report"
	@echo "  test-watch  - Run tests in watch mode"
	@echo ""
	@echo "Utility Commands:"
	@echo "  clean       - Clean up cache files and build artifacts"
	@echo "  deps        - Show dependency tree"
	@echo "  info        - Show project information"
	@echo ""
	@echo "Example workflow:"
	@echo "  make setup && make dev    # First time setup"
	@echo "  make test && make check   # Before committing"

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip setuptools wheel
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements-dev.txt
	@echo ""
	@echo "✅ Setup complete! Activate with: source .venv/bin/activate"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

lint:
	ruff check .
	pyright .

format:
	ruff format .
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/

server:
	python -m src.server

check:
	ruff check .
	ruff format --check .
	pyright .

# Enhanced development targets
dev: install-dev
	@echo "🚀 Starting development mode..."
	@echo "📦 Dependencies installed"
	@echo "🔧 Running LSP server..."
	python -m src.server

run: server

watch:
	@echo "👀 Starting server in watch mode (restart on file changes)..."
	@which inotifywait > /dev/null || (echo "Installing inotify-tools..." && sudo apt-get install -y inotify-tools)
	@while true; do \
		python -m src.server & \
		SERVER_PID=$$!; \
		inotifywait -r -e modify,create,delete --exclude '(__pycache__|\.pyc$$|\.git)' .; \
		echo "🔄 Files changed, restarting server..."; \
		kill $$SERVER_PID 2>/dev/null || true; \
		sleep 1; \
	done

test-watch:
	@echo "👀 Running tests in watch mode..."
	@which pytest-watch > /dev/null || pip install pytest-watch
	ptw tests/ -- -v

fix:
	@echo "🔧 Auto-fixing code issues..."
	ruff check --fix .
	ruff format .

# Utility targets
deps:
	@echo "📦 Dependency tree:"
	pip list

info:
	@echo "📋 Project Information"
	@echo "======================"
	@echo "Python version: $$(python --version)"
	@echo "Pip version: $$(pip --version)"
	@echo "Virtual env: $$(which python)"
	@echo "Project root: $$(pwd)"
	@echo "Ruff version: $$(ruff --version 2>/dev/null || echo 'Not installed')"
	@echo "Pyright version: $$(pyright --version 2>/dev/null || echo 'Not installed')"

# CI/CD and workflow targets
ci: install-dev check test
	@echo "🎉 All CI checks passed!"

quick-test: fix test
	@echo "🚀 Quick development cycle complete!"

pre-commit: fix lint test
	@echo "✅ Pre-commit checks complete!"
