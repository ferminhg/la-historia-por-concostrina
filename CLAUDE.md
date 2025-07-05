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
make test          # Run tests
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

### Podcast Crawler (Hexagonal Architecture)
- **Domain Layer**: Core entities (Podcast, Episode) and repository interfaces
- **Application Layer**: Use cases like CrawlPodcastUseCase
- **Infrastructure Layer**: File-based repository implementation
- **App Layer**: CLI entry point and argument parsing

### Key Files Structure
```
podcast_crawler/
├── app/crawler.py                     # Main CLI application
├── domain/
│   ├── entities/podcast.py           # Podcast and Episode entities
│   └── repositories/podcast_repository.py  # Repository interface
├── application/use_cases/crawl_podcast.py  # Business logic
└── infrastructure/repositories/file_podcast_repository.py  # File storage
```

### Data Flow
1. RSS feeds are downloaded and parsed (scrapping_episodies.ipynb)
2. Audio files are downloaded to `audios/` directory
3. Audio transcriptions are generated using OpenAI API (audio_transcriptions.ipynb)
4. Transcriptions are saved to `transcriptions/` directory
5. Episode metadata is stored in `data/episodes.json`

## Dependencies

### Core Dependencies
- **requests**: HTTP requests for RSS feeds and audio downloads
- **feedparser**: RSS feed parsing
- **openai**: Audio transcription via OpenAI API
- **supabase**: Database integration
- **pandas/numpy**: Data manipulation
- **pytorch/transformers**: ML model support

### Development Dependencies
- **pytest**: Testing framework
- **jupyterlab**: Notebook environment

## Environment Variables

Required environment variables (use .env file):
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Data Sources

The project crawls two RSS feeds:
1. `https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml`
2. `https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml`

## File Naming Convention

Audio files are named using the format: `YYYY_MM_DD_HH.mp3` based on the episode's publication date.

## Note on Implementation Status

The podcast crawler is in early development - core functionality like RSS parsing and audio downloading is implemented in the Jupyter notebooks, but the hexagonal architecture components are mostly placeholder code requiring implementation.

## Development Guidelines

- **Code Comments**: 
  - Stop adding unnecessary comments in code