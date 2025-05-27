# Make + Python: Common Patterns and Best Practices

## Why Make Works Great with Python

### 1. **Task Automation**

```makefile
# Instead of remembering complex commands:
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# Just use:
make test-cov
```

### 2. **Environment Management**

```makefile
# Automatically activate venv for each command
setup:
 python3 -m venv .venv
 .venv/bin/pip install -r requirements.txt

test: .venv
 .venv/bin/python -m pytest
```

### 3. **Dependency Tracking**

```makefile
# Only rebuild when requirements change
.venv: requirements.txt
 python3 -m venv .venv
 .venv/bin/pip install -r requirements.txt
 touch .venv
```

## Popular Python Project Patterns

### Django Projects

```makefile
migrate:
 python manage.py migrate

runserver:
 python manage.py runserver

collectstatic:
 python manage.py collectstatic --noinput

test:
 python manage.py test
```

### Data Science Projects

```makefile
notebook:
 jupyter lab

data-clean:
 python scripts/clean_data.py

train:
 python train_model.py

visualize:
 python generate_plots.py
```

### API Projects

```makefile
dev:
 uvicorn main:app --reload

docker-build:
 docker build -t myapi .

docker-run:
 docker run -p 8000:8000 myapi

deploy:
 docker push myregistry/myapi:latest
```

## Advanced Make Features for Python

### 1. **Variables and Configuration**

```makefile
PYTHON := python3
VENV := .venv
PORT := 8000

dev:
 $(PYTHON) -m uvicorn main:app --port $(PORT) --reload
```

### 2. **Conditional Logic**

```makefile
install:
ifeq ($(ENV), production)
 pip install -r requirements.txt
else
 pip install -r requirements-dev.txt
endif
```

### 3. **File Pattern Rules**

```makefile
# Convert all .py files to .pyc
%.pyc: %.py
 python -m py_compile $<
```

## Integration with Modern Python Tools

### With Poetry

```makefile
install:
 poetry install

test:
 poetry run pytest

lint:
 poetry run ruff check .
```

### With Docker

```makefile
docker-test:
 docker-compose run --rm app pytest

docker-lint:
 docker-compose run --rm app ruff check .
```

### With Pre-commit

```makefile
pre-commit-install:
 pre-commit install

pre-commit-run:
 pre-commit run --all-files
```

## Best Practices

1. **Use .PHONY for non-file targets**
2. **Add help as default target**
3. **Use variables for common paths/commands**
4. **Add emoji for better UX** 🚀
5. **Group related tasks logically**
6. **Add error handling with || true**
7. **Use @ to hide command output when appropriate**

## Example Professional Makefile Structure

```makefile
# Variables
PYTHON := python3
VENV := .venv
SRC := pseint_lsp/

# Phony targets
.PHONY: help install test lint format clean

# Default target
help:
 @echo "Available commands:"
 @echo "  install  - Install dependencies"
 @echo "  test     - Run tests"
 @echo "  lint     - Run linting"

# Environment setup
$(VENV): requirements.txt
 $(PYTHON) -m venv $(VENV)
 $(VENV)/bin/pip install -r requirements.txt

# Development tasks
install: $(VENV)

test: $(VENV)
 $(VENV)/bin/python -m pytest

lint: $(VENV)
 $(VENV)/bin/ruff check $(SRC)

format: $(VENV)
 $(VENV)/bin/ruff format $(SRC)

clean:
 rm -rf $(VENV) __pycache__ .pytest_cache
```

## Alternatives to Consider

While Make is excellent, also consider:

- **Just** (modern command runner)
- **Invoke** (Python-based task runner)
- **Tox** (Python testing automation)
- **npm scripts** (if you have Node.js anyway)

But Make remains the most universal and widely supported option!
