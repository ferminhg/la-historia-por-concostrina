# Cost Tracking for OpenAI Transcriptions

This module provides comprehensive cost tracking for OpenAI Whisper API usage.

## Features

- **Automatic Cost Calculation**: Tracks costs based on audio duration (Whisper charges ~$0.006/minute)
- **Persistent Storage**: Stores cost data in JSON files for historical tracking
- **Cost Reporting**: Provides total cost summaries and per-episode breakdowns
- **Integration**: Seamlessly integrated with existing transcription workflow

## Usage

### Basic Usage with Cost Tracking

```bash
# Run with OpenAI transcriptor and cost tracking
make run-embedder-openai

# Or manually
python -m app.main --command process --transcriptor openai
```

### Dry Run with Cost Tracking

```bash
# Test with a single episode
make dry-run-embedder-openai

# Or manually  
python -m app.main --command process --transcriptor openai --dry-run
```

## Data Storage

Cost data is stored in `audio_embedder/data/costs/` with the following structure:

```
data/costs/
├── 20240903_190633_cost.json
├── 20240904_183045_cost.json
└── ...
```

Each cost file contains:
```json
{
  "episode_id": "20240903_190633",
  "duration_minutes": 45.2,
  "cost_usd": "0.2712", 
  "api_model": "whisper-1",
  "created_at": "2025-07-06T09:43:24.447000"
}
```

## Cost Reporting

The system automatically logs:
- Cost per episode during transcription
- Total accumulated costs at the end of processing
- Warning when cost data already exists (preventing duplicates)

Example output:
```
Cost tracking: $0.2712 for 45.20 minutes (episode: Historia de España - Episodio 123)
💰 Total OpenAI transcription costs: $15.4560
```

## Cost Calculation

- **Rate**: $0.006 per minute of audio
- **Precision**: Uses Decimal for accurate financial calculations
- **Deduplication**: Prevents double-charging for already processed episodes

## Integration Points

### OpenAIAudioTranscriptor
- Calculates cost based on episode duration
- Saves cost data after successful transcription
- Logs detailed cost information

### ProcessEpisodesUseCase  
- Displays total cost summary at completion
- Only tracks costs when using OpenAI transcriptor

### Main Application
- Automatically sets up cost repository for OpenAI transcriptor
- Configurable cost data directory via `--costs-dir` parameter

## Utility Functions

The `CostUtils` class provides additional reporting:
- Daily cost summaries
- Monthly cost summaries  
- Formatted cost reports with averages

## Architecture

Follows hexagonal architecture principles:
- **Domain**: `Cost` entity and `CostRepository` interface
- **Infrastructure**: `FileCostRepository` for JSON file storage
- **Application**: Integration with transcription workflow