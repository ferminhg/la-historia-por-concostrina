# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a podcast analysis project for "La Historia Por Concostrina," a Spanish history podcast. The project consists of:

1. **Podcast Crawler** - A Python package using hexagonal architecture for downloading and processing podcast episodes
2. **Audio Processing** - Jupyter notebooks for transcription and analysis of podcast episodes
3. **Data Storage** - Structured storage of episodes, transcriptions, and audio files

## Environment Setup

### Conda Environment
```bash
conda env create -f notebooks/enviroments.yml
conda activate la-historia-por-concostrina
```

### Python Package (podcast_crawler)
```bash
cd podcast_crawler
pip install -e .
```

## Development Commands

### Using Make (Recommended)
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
```

### Manual Commands
```bash
# From podcast_crawler directory
python -m app.crawler

# Or directly with entry point
podcast-crawler
```

### Running Tests
```bash
# From podcast_crawler directory
pytest tests/
# Or with verbose output
pytest -v tests/

# Run specific test
pytest tests/test_xml_processor.py::TestXMLProcessor::test_parses_duration_formats -v
```

### Jupyter Notebooks
```bash
# Start JupyterLab
jupyter lab

# Key notebooks:
# - notebooks/scrapping_episodies.ipynb - Downloads RSS feeds and episode metadata
# - notebooks/audio_transcriptions.ipynb - Transcribes audio using OpenAI API
```

## Architecture

### Hexagonal Architecture Implementation

The project implements hexagonal architecture with clear separation of concerns:

**Domain Layer** (`domain/`):
- `entities/` - Core business entities (Episode, Podcast, RSSUrl)
- `repositories/` - Repository interfaces for data access
- `builders/` - Builder pattern for immutable entity updates

**Application Layer** (`application/`):
- `use_cases/` - Business logic orchestration (CrawlPodcastUseCase)
- `services/` - Application services (EpisodeDownloader)

**Infrastructure Layer** (`infrastructure/`):
- `repositories/` - Concrete repository implementations
- `xml/` - XML processing with iTunes namespace support
- `logging/` - Custom logging abstraction

**Shared** (`shared/`):
- Common utilities and abstractions used across layers

### Key Components

**Episode Processing Pipeline**:
1. `HardcodedRSSUrlRepository` downloads RSS feeds to XML files
2. `XMLProcessor` parses XML with iTunes namespace support, extracts Episode entities
3. `EpisodeDownloader` downloads audio files and updates Episode with local file paths
4. `LocalFileEpisodeRepository` handles local file storage with date-based naming

**Logging System**:
- Custom logging abstraction in `infrastructure/logging/`
- Import via `from shared.logger import get_logger`
- Configured for structured logging with timestamps

**Testing**:
- `tests/helpers/podcast_mother.py` - Test data builders using Object Mother pattern
- Comprehensive test coverage for XML processing, episode downloading, and logging

### Data Flow

1. RSS feeds downloaded from hardcoded URLs
2. XML parsed to extract episodes with iTunes duration and file size
3. Episodes downloaded to `audios/` directory with format `YYYY_MM_DD_HH.mp3`
4. Episode entities updated immutably with local file paths using builder pattern
5. Existing files skipped to avoid re-downloads

## Dependencies

### Core Dependencies
- **requests**: HTTP requests for RSS feeds and audio downloads  
- **ruff**: Code formatting and linting
- **pytest**: Testing framework

### Development Dependencies
- **pytest-cov**: Test coverage
- **jupyterlab**: Notebook environment for data analysis

## Environment Variables

Required for audio transcription notebooks:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Data Sources

The project crawls two RSS feeds:
1. `https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml`
2. `https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml`

## File Naming Convention

Audio files are named using the format: `YYYY_MM_DD_HH.mp3` based on the episode's publication date.

## Development Guidelines

- **Code Style**: Use English for all programming code
- **Comments**: Avoid unnecessary comments in code
- **Immutability**: Use builder pattern for entity updates (see `EpisodeBuilder`)
- **Testing**: Use Object Mother pattern for test data creation
- **Logging**: Use custom logger abstraction, not direct Python logging