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
make run-crawler          # Run podcast crawler
make run-embedder         # Run audio embedder (mock transcriptor)
make run-embedder-openai  # Run audio embedder (OpenAI transcriptor)

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
make search        # Search episodes

# Manual execution
python -m app.main --command process --transcriptor mock
python -m app.main --command process --transcriptor openai
python -m app.main --command search --query "your search query"
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

### Jupyter Notebooks
```bash
# Start JupyterLab
jupyter lab

# Key notebooks:
# - notebooks/scrapping_episodies.ipynb - Downloads RSS feeds and episode metadata (deprecated)
# - notebooks/audio_transcriptions.ipynb - Transcribes audio using OpenAI API
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
2. `AudioTranscriptor` creates transcriptions from audio files
3. `FileTranscriptionRepository` stores transcriptions in `audio_embedder/data/transcriptions/`
4. `EmbeddingService` chunks text and creates vector embeddings
5. `EmbeddingRepository` stores embeddings for semantic search
6. `SearchEpisodesUseCase` enables semantic search across episode content

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
- Transcribes audio files using `AudioTranscriptor`
- Creates vector embeddings for semantic search
- Enables search functionality across podcast content

### Testing Architecture

Both packages use consistent testing patterns:
- `tests/helpers/*_mother.py` - Test data builders using Object Mother pattern
- Mock implementations for external services (transcription, embedding)
- Comprehensive test coverage for use cases, repositories, and services

## Dependencies

### Shared Dependencies (requirements.txt)
- **requests**: HTTP requests for RSS feeds and audio downloads  
- **openai**: OpenAI API client for audio transcription
- **feedparser**: RSS feed parsing
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting
- **ruff**: Code formatting and linting

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
└── embeddings/          # Vector embeddings storage
```

## Development Guidelines

- **Code Style**: Use English for all programming code
- **Comments**: Avoid unnecessary comments in code
- **Immutability**: Use builder pattern for entity updates (see `EpisodeBuilder`)
- **Testing**: Use Object Mother pattern for test data creation
- **Logging**: Use custom logger abstraction via `from shared.logger import get_logger`
- **Architecture**: Follow hexagonal architecture patterns for both packages
- **Mock First**: audio_embedder currently uses mock implementations for transcription and embedding services