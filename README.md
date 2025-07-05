# La Historia Por Concostrina - Podcast Analysis Project

A podcast analysis project for "La Historia Por Concostrina," a Spanish history podcast. The project consists of a Python package using hexagonal architecture for downloading and processing podcast episodes, along with Jupyter notebooks for transcription and analysis.

## Project Structure

- **podcast_crawler/** - Python package implementing hexagonal architecture
- **notebooks/** - Jupyter notebooks for audio transcription and analysis
- **data/** - RSS feeds and episode metadata storage
- **audios/** - Downloaded podcast audio files

## Quick Start

### Environment Setup

```bash
# Create conda environment
conda env create -f notebooks/enviroments.yml
conda activate la-historia-por-concostrina

# Install Python package
cd podcast_crawler
pip install -e .
```

### Development Commands

```bash
# From podcast_crawler directory
make help          # Show all available commands
make install       # Install dependencies and package
make tests         # Run tests
make lint          # Run linting with ruff
make format        # Format code with ruff
make run           # Run the podcast crawler
```

### Running the Crawler

```bash
# From podcast_crawler directory
make run
# Or manually
python -m app.crawler
# Or with entry point
podcast-crawler
```

## Architecture

The project implements hexagonal architecture with clear separation of concerns:

- **Domain Layer** - Core business entities (Episode, Podcast, RSSUrl)
- **Application Layer** - Business logic orchestration and services
- **Infrastructure Layer** - Repository implementations and external integrations

## Data Sources

The project crawls two RSS feeds:
1. `https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml`
2. `https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml`

## File Naming Convention

Audio files are named using the format: `YYYY_MM_DD_HH.mp3` based on the episode's publication date.

## Development

### Testing
```bash
pytest tests/
```

### Jupyter Notebooks
```bash
jupyter lab
```

Key notebooks:
- `notebooks/scrapping_episodies.ipynb` - Downloads RSS feeds and episode metadata
- `notebooks/audio_transcriptions.ipynb` - Transcribes audio using OpenAI API

## Environment Variables

For audio transcription:
```
OPENAI_API_KEY=your_openai_api_key_here
```
