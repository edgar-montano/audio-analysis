.PHONY: help install dev clean test build publish

help:
	@echo "Available commands:"
	@echo "  make install    - Install the package"
	@echo "  make dev        - Install with development dependencies"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make test       - Run tests (when available)"
	@echo "  make build      - Build distribution packages"
	@echo "  make publish    - Publish to PyPI"
	@echo "  make test-pypi  - Publish to TestPyPI"

install:
	uv sync

dev:
	uv sync --all-extras

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	@echo "No test suite configured yet. See CONTRIBUTING.md"

build: clean
	python -m build

publish: build
	twine upload dist/*

test-pypi: build
	twine upload --repository testpypi dist/*
