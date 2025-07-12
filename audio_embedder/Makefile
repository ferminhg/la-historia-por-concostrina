.PHONY: help install tests lint format sort-imports clean run run-openai dry-run dry-run-openai search transcriptions-to-embeddings dry-run-transcriptions-to-embeddings transcriptions-to-embeddings-supabase dry-run-transcriptions-to-embeddings-supabase search-supabase episode-summary

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
	@echo "  transcriptions-to-embeddings     - Convert existing transcriptions to embeddings"
	@echo "  dry-run-transcriptions-to-embeddings - Convert transcriptions to embeddings in dry-run mode"
	@echo "  transcriptions-to-embeddings-supabase - Convert transcriptions to embeddings using Supabase"
	@echo "  dry-run-transcriptions-to-embeddings-supabase - Convert transcriptions to embeddings using Supabase in dry-run mode"
	@echo "  search-supabase - Search episodes in Supabase (requires --query)"
	@echo "  episode-summary - Show episode summary (requires EPISODE_ID env var)"

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

transcriptions-to-embeddings:
	python -m app.main --command transcriptions-to-embeddings

dry-run-transcriptions-to-embeddings:
	python -m app.main --command transcriptions-to-embeddings --dry-run

transcriptions-to-embeddings-supabase:
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	python -m app.main --command transcriptions-to-embeddings --use-supabase

dry-run-transcriptions-to-embeddings-supabase:
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	python -m app.main --command transcriptions-to-embeddings --use-supabase --dry-run

search-supabase:
	@echo "🔍 Searching in Supabase..."
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	@if [ -z "$(QUERY)" ]; then \
		echo "❌ Error: QUERY variable is required. Usage: make search-supabase QUERY='your search query'"; \
		echo "📝 Optional: EPISODE_ID='episode_id' TOP_K=5"; \
		exit 1; \
	fi
	@if [ -n "$(EPISODE_ID)" ]; then \
		python -m app.main --command search-supabase --query "$(QUERY)" --episode-id "$(EPISODE_ID)" --top-k $(if $(TOP_K),$(TOP_K),5); \
	else \
		python -m app.main --command search-supabase --query "$(QUERY)" --top-k $(if $(TOP_K),$(TOP_K),5); \
	fi

episode-summary:
	@echo "📊 Getting episode summary..."
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	@if [ -z "$(EPISODE_ID)" ]; then \
		echo "❌ Error: EPISODE_ID variable is required. Usage: make episode-summary EPISODE_ID='20240520_190000'"; \
		exit 1; \
	fi
	python -m app.main --command search-supabase --episode-id "$(EPISODE_ID)" --show-summary