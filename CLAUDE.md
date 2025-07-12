# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a podcast analysis project for "La Historia Por Concostrina," a Spanish history podcast. The project consists of:

1. **Podcast Crawler** - A Python package using hexagonal architecture for downloading and processing podcast episodes
2. **Audio Embedder** - A Python package for transcribing episodes and creating vector embeddings for semantic search
3. **Audio Processing** - Jupyter notebooks for transcription and analysis of podcast episodes
4. **Data Storage** - Structured storage of episodes, transcriptions, embeddings, and audio files

## Environment Setup

### Conda Environment
```bash
conda env create -f notebooks/enviroments.yml
conda activate la-historia-por-concostrina
```

### Python Packages
```bash
# Install all packages from root directory (recommended)
make install

# Or install individually
cd podcast_crawler && pip install -e .
cd audio_embedder && pip install -e .

# Or install specific packages
make install-crawler    # Only podcast_crawler
make install-embedder   # Only audio_embedder
```

## Development Commands

### Global Commands (from root directory)
```bash
make help                 # Show all available commands
make install              # Install all dependencies and packages
make tests                # Run all tests
make lint                 # Run linting on all packages
make format               # Format code in all packages
make clean                # Clean temporary files

# Run applications
make run-crawler            # Run podcast crawler
make run-embedder           # Run audio embedder (mock transcriptor)
make run-embedder-openai    # Run audio embedder (OpenAI transcriptor)
make dry-run-embedder       # Run audio embedder in dry-run mode (mock, 1 episode)
make dry-run-embedder-openai # Run audio embedder in dry-run mode (OpenAI, 1 episode)
make transcriptions-to-embeddings     # Convert existing transcriptions to embeddings
make dry-run-transcriptions-to-embeddings # Convert transcriptions to embeddings in dry-run mode
make transcriptions-to-embeddings-supabase # Convert transcriptions to embeddings using Supabase
make dry-run-transcriptions-to-embeddings-supabase # Convert transcriptions to embeddings using Supabase in dry-run mode
make search-supabase QUERY='search term'     # Search episodes in Supabase
make episode-summary EPISODE_ID='episode_id' # Get episode summary from Supabase

# Individual package installation
make install-crawler      # Install only podcast_crawler
make install-embedder     # Install only audio_embedder

# Individual package testing
make tests-crawler        # Run only podcast_crawler tests
make tests-embedder       # Run only audio_embedder tests
```

### Package-Specific Commands

**Podcast Crawler** (from `podcast_crawler/` directory):
```bash
make help          # Show package-specific commands
make install       # Install dependencies and package
make tests         # Run tests
make lint          # Run linting with ruff
make format        # Format code with ruff
make sort-imports  # Sort imports with ruff
make clean         # Clean temporary files
make run           # Run the podcast crawler

# Manual execution
python -m app.crawler
# Or with entry point
podcast-crawler
```

**Audio Embedder** (from `audio_embedder/` directory):
```bash
make help          # Show package-specific commands
make install       # Install dependencies and package
make tests         # Run tests
make lint          # Run linting with ruff
make format        # Format code with ruff
make sort-imports  # Sort imports with ruff
make clean         # Clean temporary files
make run           # Run episode processing (mock transcriptor)
make run-openai    # Run with OpenAI transcriptor
make dry-run       # Run in dry-run mode (mock, 1 episode)
make dry-run-openai # Run in dry-run mode (OpenAI, 1 episode)
make search        # Search episodes
make transcriptions-to-embeddings     # Convert existing transcriptions to embeddings
make dry-run-transcriptions-to-embeddings # Convert transcriptions to embeddings in dry-run mode
make transcriptions-to-embeddings-supabase # Convert transcriptions to embeddings using Supabase
make dry-run-transcriptions-to-embeddings-supabase # Convert transcriptions to embeddings using Supabase in dry-run mode
make search-supabase QUERY='search term'     # Search episodes in Supabase
make episode-summary EPISODE_ID='episode_id' # Get episode summary from Supabase

# Manual execution
python -m app.main --command process --transcriptor mock
python -m app.main --command process --transcriptor openai
python -m app.main --command process --transcriptor mock --dry-run
python -m app.main --command process --transcriptor openai --dry-run
python -m app.main --command search --query "your search query"
python -m app.main --command transcriptions-to-embeddings
python -m app.main --command transcriptions-to-embeddings --dry-run
python -m app.main --command transcriptions-to-embeddings --use-supabase
python -m app.main --command transcriptions-to-embeddings --use-supabase --dry-run
python -m app.main --command search-supabase --query "Iglesia catolica"
python -m app.main --command search-supabase --query "search term" --episode-id "20240520_190000"
python -m app.main --command search-supabase --episode-id "20240520_190000" --show-summary
```

### Running Tests
```bash
# All tests from root
make tests

# Individual package tests
make tests-crawler
make tests-embedder

# Or manually
cd podcast_crawler && pytest tests/ -v
cd audio_embedder && pytest tests/ -v

# Specific test
pytest tests/test_xml_processor.py::TestXMLProcessor::test_parses_duration_formats -v
```

### Supabase Vector Search
```bash
# Search across all episodes
make search-supabase QUERY='Iglesia catolica'
make search-supabase QUERY='Guerra Civil' TOP_K=10

# Search within specific episode
make search-supabase QUERY='Francisco Franco' EPISODE_ID='20240520_190000'

# Get episode summary and statistics
make episode-summary EPISODE_ID='20240520_190000'

# Manual execution with more options
python -m app.main --command search-supabase --query "your search" --top-k 5
python -m app.main --command search-supabase --query "search" --episode-id "episode_id" --top-k 3
python -m app.main --command search-supabase --episode-id "episode_id" --show-summary
```

### Jupyter Notebooks
```bash
# Start JupyterLab
jupyter lab

# Key notebooks:
# - notebooks/scrapping_episodies.ipynb - Downloads RSS feeds and episode metadata (deprecated)
# - notebooks/audio_transcriptions.ipynb - Transcribes audio using OpenAI API
# - notebooks/transcription_embedders.ipynb - Supabase vector search implementation
```

## Architecture

Both `podcast_crawler` and `audio_embedder` implement hexagonal architecture with clear separation of concerns:

### Hexagonal Architecture Layers

**Domain Layer** (`domain/`):
- `entities/` - Core business entities (Episode, Podcast, RSSUrl, Transcription, Embedding)
- `repositories/` - Repository interfaces for data access
- `builders/` - Builder pattern for immutable entity updates

**Application Layer** (`application/`):
- `use_cases/` - Business logic orchestration (CrawlPodcastUseCase, ProcessEpisodesUseCase, SearchEpisodesUseCase)
- `services/` - Application services (EpisodeDownloader, AudioTranscriptor, EmbeddingService)

**Infrastructure Layer** (`infrastructure/`):
- `repositories/` - Concrete repository implementations
- `xml/` - XML processing with iTunes namespace support (podcast_crawler)
- `transcriptor/` - Audio transcription implementations (audio_embedder)
- `embedder/` - Vector embedding implementations (audio_embedder)
- `logging/` - Custom logging abstraction

**Shared** (`shared/`):
- Common utilities and abstractions used across layers

### Key Processing Pipelines

**Podcast Crawling Pipeline** (podcast_crawler):
1. `HardcodedRSSUrlRepository` downloads RSS feeds to XML files in `data/`
2. `XMLProcessor` parses XML with iTunes namespace support, extracts Episode entities
3. `EpisodeDownloader` downloads audio files to `audios/` directory with format `YYYY_MM_DD_HH.mp3`
4. `LocalFileEpisodeRepository` handles local file storage with date-based naming
5. `JSONEpisodeRepository` saves episode metadata to `data/episodes.json`
6. Existing files skipped to avoid re-downloads

**Audio Embedding Pipeline** (audio_embedder):
1. `JSONEpisodeRepository` reads episodes from `data/episodes.json`
2. `AudioTranscriptor` creates transcriptions from audio files (OpenAI or Mock)
3. `FileTranscriptionRepository` stores transcriptions in `audio_embedder/data/transcriptions/`
4. `EmbeddingService` chunks text and creates vector embeddings
5. `EmbeddingRepository` stores embeddings for semantic search
6. `SearchEpisodesUseCase` enables semantic search across episode content

**Dry-Run Mode**: Process only the first episode without saving data, useful for testing transcription services and validating API credentials.

### Data Flow Architecture

```
RSS Feeds → podcast_crawler → episodes.json + audio files → audio_embedder → transcriptions + embeddings
```

**Stage 1: Data Collection** (podcast_crawler)
- Downloads RSS feeds from hardcoded URLs to `data/feed_*.xml`
- Extracts episode metadata and downloads audio files
- Stores structured episode data in `data/episodes.json`

**Stage 2: Content Processing** (audio_embedder)
- Reads episode metadata from `data/episodes.json`
- Transcribes audio files using `AudioTranscriptor` (OpenAI or Mock)
- Creates vector embeddings for semantic search
- Enables search functionality across podcast content
- Supports dry-run mode for testing without data persistence

### Testing Architecture

Both packages use consistent testing patterns:
- `tests/helpers/*_mother.py` - Test data builders using Object Mother pattern
- Mock implementations for external services (transcription, embedding)
- Comprehensive test coverage for use cases, repositories, and services

### Audio Embedder Specific Patterns

**Transcription Services**:
- `MockAudioTranscriptor` - Fast placeholder transcriptions for development
- `OpenAIAudioTranscriptor` - Production transcription using OpenAI's `gpt-4o-mini-transcribe` model
- Streaming transcription support for real-time processing

**Cost Tracking**:
- `FileCostRepository` - Tracks OpenAI API costs with persistent JSON storage
- Automatic cost calculation based on audio duration (~$0.006/minute)
- Cost deduplication to prevent double-charging
- Total cost reporting and daily/monthly summaries

**Repository Patterns**:
- `JSONEpisodeRepository` - Reads centralized episode metadata
- `FileTranscriptionRepository` - Hash-based file storage for transcriptions
- `MockEmbeddingRepository` - In-memory storage for development/testing

**Use Case Patterns**:
- `ProcessEpisodesUseCase` - Orchestrates transcription and embedding pipeline
- `SearchEpisodesUseCase` - Semantic search across transcribed content (local storage)
- `TranscriptionsToEmbeddingsUseCase` - Converts existing transcriptions to embeddings with semantic chunking
- `SearchSupabaseUseCase` - Direct semantic search in Supabase vector database
- Dry-run mode support in processing use cases

**Enhanced Features**:
- `SemanticChunker` - Advanced text chunking for podcast transcriptions with topic boundary detection
- `SupabaseEmbeddingService` - OpenAI embeddings with Supabase vector storage integration
- Supports both local mock storage and Supabase vector database
- Episode-specific search and summary functionality

## Dependencies

### Shared Dependencies (requirements.txt)
- **requests**: HTTP requests for RSS feeds and audio downloads  
- **langchain**: LLM framework for audio transcription and AI processing
- **langchain-openai**: OpenAI integration for langchain
- **langchain-community**: Community tools and utilities for langchain
- **feedparser**: RSS feed parsing
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting
- **ruff**: Code formatting and linting
- **python-dotenv**: Environment variable management

### Conda Environment Dependencies (notebooks/enviroments.yml)
- **Python 3.11**: Base runtime
- **Data Science Stack**: numpy, pandas, scipy, matplotlib, scikit-learn
- **ML/AI Libraries**: pytorch, transformers, librosa, datasets, accelerate
- **Vector Storage**: chromadb, faiss-cpu
- **Audio Processing**: librosa, sentencepiece
- **APIs**: openai, supabase
- **Notebooks**: jupyterlab, ipywidgets, jupyter-dash

## Environment Variables

Required for audio transcription functionality:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Required for Supabase embeddings functionality:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

## Data Sources

The project crawls two RSS feeds:
1. `https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml`
2. `https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml`

## Data Storage Structure

```
data/
├── episodes.json          # Centralized episode metadata (output of podcast_crawler)
├── feed_*.xml            # Downloaded RSS feeds
└── audios/               # Downloaded audio files (YYYY_MM_DD_HH.mp3 format)

audio_embedder/data/
├── transcriptions/       # Episode transcriptions (hash-based JSON files)
├── embeddings/          # Vector embeddings storage
└── costs/               # OpenAI API cost tracking data
```

## Development Guidelines

- **Code Style**: Use English for all programming code
- **Comments**: Avoid unnecessary comments in code
- **Immutability**: Use builder pattern for entity updates (see `EpisodeBuilder`)
- **Testing**: Use Object Mother pattern for test data creation
- **Logging**: Use custom logger abstraction via `from shared.logger import get_logger`
- **Architecture**: Follow hexagonal architecture patterns for both packages
- **Type Annotations**: Use modern Python type hints (`list[T]` instead of `List[T]`)
- **Mock First**: audio_embedder provides both mock and real implementations for transcription services
- **Dry-Run Testing**: Use `--dry-run` flag to test transcription services without persisting data