.PHONY: help install tests lint format sort-imports clean run

help:
	@echo "Available commands: 🛠️"
	@echo "  install       - Install dependencies and package in development mode 📦"
	@echo "  tests         - Run tests with pytest 🧪"
	@echo "  lint          - Run linting with ruff 🔍"
	@echo "  format        - Format code with ruff 🎨"
	@echo "  sort-imports  - Sort imports with ruff 📚"
	@echo "  clean         - Clean temporary files 🧹"
	@echo "  run           - Run the crawler 🚀"
	@echo "  help          - Show this help ℹ️"

install:
	@echo "Installing dependencies... 📦"
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Installation completed"

tests:
	@echo "Running tests... 🧪"
	pytest tests/ -v
	@echo "✅ Tests completed"

lint:
	@echo "Running linting... 🔍"
	ruff check .
	@echo "✅ Linting completed"

format:
	@echo "Formatting code... 🎨"
	ruff format .
	@echo "✅ Formatting completed"

sort-imports:
	@echo "Sorting imports... 📚"
	ruff check --select I --fix .
	@echo "✅ Imports sorted"

clean:
	@echo "Cleaning temporary files... 🧹"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean completed"

run:
	@echo "Running podcast crawler... 🚀"
	python -m app.crawler