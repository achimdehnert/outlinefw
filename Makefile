# Python Package — Developer Makefile

.PHONY: install test test-v lint format mypy check clean build help

PYTHON := python3
PIP    := pip

help:
	@echo "Available targets:"
	@echo "  install   — pip install in dev mode"
	@echo "  test      — pytest (quiet)"
	@echo "  test-v    — pytest (verbose)"
	@echo "  lint      — ruff check + format --check (matches CI)"
	@echo "  format    — ruff format (apply)"
	@echo "  mypy      — mypy strict type-check"
	@echo "  check     — lint + mypy + test (full local gate = CI)"
	@echo "  build     — build wheel + sdist"
	@echo "  clean     — remove build artifacts"

install:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest --tb=short -q

test-v:
	$(PYTHON) -m pytest --tb=short -v

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff format src/ tests/

mypy:
	$(PYTHON) -m mypy

check: lint mypy test

build:
	$(PYTHON) -m build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info/
	@echo "Cleaned."
