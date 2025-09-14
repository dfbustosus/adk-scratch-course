# Makefile for ADK Toolkit development

.PHONY: help install install-dev test lint format check clean docs serve-docs build publish

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install the package for production"
	@echo "  install-dev  Install the package with development dependencies"
	@echo "  test         Run all tests"
	@echo "  test-unit    Run unit tests only"
	@echo "  test-cov     Run tests with coverage report"
	@echo "  lint         Run all linting tools"
	@echo "  format       Format code with black and isort"
	@echo "  check        Run all quality checks"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Build documentation"
	@echo "  serve-docs   Serve documentation locally"
	@echo "  build        Build distribution packages"
	@echo "  publish      Publish to PyPI (use with caution!)"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest

test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

test-cov:
	pytest --cov=src/adk --cov-report=html --cov-report=term

# Linting and formatting
format:
	black src/ tests/
	isort src/ tests/

lint:
	black --check src/ tests/
	isort --check-only src/ tests/
	flake8 src/ tests/
	mypy src/


# Quality checks
check: format lint test

# Documentation
docs:
	cd docs && make html

serve-docs:
	cd docs && make html && python -m http.server 8000 --directory _build/html

clean-docs:
	cd docs && make clean

# Build and publish
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python3 -m build

publish: build
	twine check dist/*
	twine upload dist/*

# Development helpers
setup:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install

validate:
	adk validate

demo:
	@echo "Scaffolding demo agent..."
	@adk scaffold demo-agent
	@echo "\nRunning demo agent..."
	@adk run demo-agent

# CI/CD helpers
ci-install:
	python -m pip install --upgrade pip
	pip install -e ".[test]"

ci-test:
	pytest --cov=src/adk --cov-report=xml --cov-report=term

ci-lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy src/
