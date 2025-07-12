.PHONY: help install install-crawler install-embedder tests tests-crawler tests-embedder lint format clean run-crawler run-embedder run-embedder-openai dry-run-embedder dry-run-embedder-openai transcriptions-to-embeddings dry-run-transcriptions-to-embeddings transcriptions-to-embeddings-supabase dry-run-transcriptions-to-embeddings-supabase search-supabase episode-summary

help:
	@echo "🎙️  La Historia Por Concostrina - Development Commands"
	@echo ""
	@echo "📦 Installation:"
	@echo "  install           - Install all dependencies and packages"
	@echo "  install-crawler   - Install only podcast_crawler"
	@echo "  install-embedder  - Install only audio_embedder"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  tests             - Run all tests"
	@echo "  tests-crawler     - Run podcast_crawler tests"
	@echo "  tests-embedder    - Run audio_embedder tests"
	@echo ""
	@echo "🛠️  Development:"
	@echo "  lint              - Run linting on all packages"
	@echo "  format            - Format code in all packages"
	@echo "  clean             - Clean temporary files in all packages"
	@echo ""
	@echo "🚀 Execution:"
	@echo "  run-crawler            - Run podcast crawler"
	@echo "  run-embedder           - Run audio embedder (mock transcriptor)"
	@echo "  run-embedder-openai    - Run audio embedder (OpenAI transcriptor)"
	@echo "  dry-run-embedder       - Run audio embedder in dry-run mode (mock, 1 episode)"
	@echo "  dry-run-embedder-openai - Run audio embedder in dry-run mode (OpenAI, 1 episode)"
	@echo "  transcriptions-to-embeddings     - Convert existing transcriptions to embeddings"
	@echo "  dry-run-transcriptions-to-embeddings - Convert transcriptions to embeddings in dry-run mode"
	@echo "  transcriptions-to-embeddings-supabase - Convert transcriptions to embeddings using Supabase"
	@echo "  dry-run-transcriptions-to-embeddings-supabase - Convert transcriptions to embeddings using Supabase in dry-run mode"
	@echo "  search-supabase      - Search episodes in Supabase (requires QUERY variable)"
	@echo "  episode-summary      - Show episode summary (requires EPISODE_ID variable)"
	@echo ""
	@echo "📚 Individual package commands available in:"
	@echo "  cd podcast_crawler && make help"
	@echo "  cd audio_embedder && make help"

install:
	@echo "📦 Installing all dependencies..."
	pip install -r requirements.txt
	@echo "📦 Installing podcast_crawler..."
	cd podcast_crawler && pip install -e .
	@echo "📦 Installing audio_embedder..."
	cd audio_embedder && pip install -e .
	@echo "✅ All packages installed successfully"

install-crawler:
	@echo "📦 Installing podcast_crawler dependencies..."
	pip install -r requirements.txt
	cd podcast_crawler && pip install -e .
	@echo "✅ podcast_crawler installed successfully"

install-embedder:
	@echo "📦 Installing audio_embedder dependencies..."
	pip install -r requirements.txt
	cd audio_embedder && pip install -e .
	@echo "✅ audio_embedder installed successfully"

tests:
	@echo "🧪 Running all tests..."
	@echo "📝 Testing podcast_crawler..."
	cd podcast_crawler && pytest tests/ -v
	@echo "📝 Testing audio_embedder..."
	cd audio_embedder && pytest tests/ -v
	@echo "✅ All tests completed"

tests-crawler:
	@echo "🧪 Running podcast_crawler tests..."
	cd podcast_crawler && pytest tests/ -v

tests-embedder:
	@echo "🧪 Running audio_embedder tests..."
	cd audio_embedder && pytest tests/ -v

lint:
	@echo "🔍 Running linting on all packages..."
	cd podcast_crawler && ruff check .
	cd audio_embedder && ruff check .
	@echo "✅ Linting completed"

format:
	@echo "🎨 Formatting code in all packages..."
	cd podcast_crawler && ruff format .
	cd audio_embedder && ruff format .
	@echo "✅ Formatting completed"

clean:
	@echo "🧹 Cleaning temporary files..."
	cd podcast_crawler && make clean
	cd audio_embedder && make clean
	@echo "✅ Clean completed"

run-crawler:
	@echo "🚀 Running podcast crawler..."
	cd podcast_crawler && python -m app.crawler

run-embedder:
	@echo "🚀 Running audio embedder (mock transcriptor)..."
	cd audio_embedder && python -m app.main --transcriptor mock

run-embedder-openai:
	@echo "🚀 Running audio embedder (OpenAI transcriptor)..."
	@echo "⚠️  Make sure OPENAI_API_KEY is set!"
	cd audio_embedder && python -m app.main --transcriptor openai

dry-run-embedder:
	@echo "🧪 Running audio embedder in DRY RUN mode (mock transcriptor)..."
	cd audio_embedder && python -m app.main --transcriptor mock --dry-run

dry-run-embedder-openai:
	@echo "🧪 Running audio embedder in DRY RUN mode (OpenAI transcriptor)..."
	@echo "⚠️  Make sure OPENAI_API_KEY is set!"
	cd audio_embedder && python -m app.main --transcriptor openai --dry-run

transcriptions-to-embeddings:
	@echo "🚀 Converting existing transcriptions to embeddings..."
	cd audio_embedder && python -m app.main --command transcriptions-to-embeddings

dry-run-transcriptions-to-embeddings:
	@echo "🧪 Converting transcriptions to embeddings in DRY RUN mode..."
	cd audio_embedder && python -m app.main --command transcriptions-to-embeddings --dry-run

transcriptions-to-embeddings-supabase:
	@echo "🚀 Converting existing transcriptions to embeddings using Supabase..."
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	cd audio_embedder && python -m app.main --command transcriptions-to-embeddings --use-supabase

dry-run-transcriptions-to-embeddings-supabase:
	@echo "🧪 Converting transcriptions to embeddings using Supabase in DRY RUN mode..."
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	cd audio_embedder && python -m app.main --command transcriptions-to-embeddings --use-supabase --dry-run

search-supabase:
	@echo "🔍 Searching episodes in Supabase..."
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	@if [ -z "$(QUERY)" ]; then \
		echo "❌ Error: QUERY variable is required."; \
		echo "💡 Usage: make search-supabase QUERY='Iglesia catolica'"; \
		echo "📝 Optional: EPISODE_ID='20240520_190000' TOP_K=5"; \
		exit 1; \
	fi
	@if [ -n "$(EPISODE_ID)" ]; then \
		cd audio_embedder && python -m app.main --command search-supabase --query "$(QUERY)" --episode-id "$(EPISODE_ID)" --top-k $(if $(TOP_K),$(TOP_K),5); \
	else \
		cd audio_embedder && python -m app.main --command search-supabase --query "$(QUERY)" --top-k $(if $(TOP_K),$(TOP_K),5); \
	fi

episode-summary:
	@echo "📊 Getting episode summary from Supabase..."
	@echo "⚠️  Make sure SUPABASE_URL and SUPABASE_KEY are set!"
	@if [ -z "$(EPISODE_ID)" ]; then \
		echo "❌ Error: EPISODE_ID variable is required."; \
		echo "💡 Usage: make episode-summary EPISODE_ID='20240520_190000'"; \
		exit 1; \
	fi
	cd audio_embedder && python -m app.main --command search-supabase --episode-id "$(EPISODE_ID)" --show-summary