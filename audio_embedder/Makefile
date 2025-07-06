.PHONY: help install tests lint format sort-imports clean run run-openai dry-run dry-run-openai search

help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies and package"
	@echo "  tests          - Run tests"
	@echo "  lint           - Run linting with ruff"
	@echo "  format         - Format code with ruff"
	@echo "  sort-imports   - Sort imports with ruff"
	@echo "  clean          - Clean temporary files"
	@echo "  run            - Run the audio embedder (mock transcriptor)"
	@echo "  run-openai     - Run the audio embedder with OpenAI transcriptor"
	@echo "  dry-run        - Run in dry-run mode (mock transcriptor, 1 episode)"
	@echo "  dry-run-openai - Run in dry-run mode (OpenAI transcriptor, 1 episode)"
	@echo "  search         - Search episodes with mock data"

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
	python -m app.main --transcriptor mock

run-openai:
	python -m app.main --transcriptor openai

dry-run:
	python -m app.main --transcriptor mock --dry-run

dry-run-openai:
	python -m app.main --transcriptor openai --dry-run

search:
	python -m app.main --command search --query "historia"