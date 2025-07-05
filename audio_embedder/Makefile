.PHONY: help install tests lint format sort-imports clean run

help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies and package"
	@echo "  tests        - Run tests"
	@echo "  lint         - Run linting with ruff"
	@echo "  format       - Format code with ruff"
	@echo "  sort-imports - Sort imports with ruff"
	@echo "  clean        - Clean temporary files"
	@echo "  run          - Run the audio embedder"

install:
	pip install -e .
	pip install -e ".[dev]"

tests:
	pytest tests/

lint:
	ruff check .

format:
	ruff format .

sort-imports:
	ruff check --fix --select I .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

run:
	python -m app.main