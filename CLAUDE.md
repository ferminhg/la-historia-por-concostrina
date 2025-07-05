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
# Install podcast_crawler
cd podcast_crawler
pip install -e .

# Install audio_embedder
cd ../audio_embedder
pip install -e .
```

## Development Commands

### Podcast Crawler
```bash
# From podcast_crawler directory
make help          # Show all available commands
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

### Audio Embedder
```bash
# From audio_embedder directory
make help          # Show all available commands
make install       # Install dependencies and package
make tests         # Run tests
make lint          # Run linting with ruff
make format        # Format code with ruff
make sort-imports  # Sort imports with ruff
make clean         # Clean temporary files
make run           # Run episode processing

# Manual execution with different commands
python -m app.main --command process  # Process episodes into transcriptions and embeddings
python -m app.main --command search --query "your search query"  # Search episodes
```

### Running Tests
```bash
# From podcast_crawler directory
pytest tests/
pytest -v tests/
pytest tests/test_xml_processor.py::TestXMLProcessor::test_parses_duration_formats -v

# From audio_embedder directory
pytest tests/
pytest -v tests/
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

### Runtime Dependencies
- **requests**: HTTP requests for RSS feeds and audio downloads  
- **ruff**: Code formatting and linting
- **pytest**: Testing framework

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