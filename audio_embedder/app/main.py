import argparse
import os
from dotenv import load_dotenv

from .application.use_cases.process_episodes import ProcessEpisodesUseCase
from .application.use_cases.search_episodes import SearchEpisodesUseCase
from .infrastructure.embedder.mock_embedding_service import MockEmbeddingService
from .infrastructure.repositories.file_transcription_repository import (
    FileTranscriptionRepository,
)
from .infrastructure.repositories.json_episode_repository import JSONEpisodeRepository
from .infrastructure.repositories.mock_embedding_repository import (
    MockEmbeddingRepository,
)
from .infrastructure.transcriptor.mock_audio_transcriptor import MockAudioTranscriptor
from .infrastructure.transcriptor.openai_audio_transcriptor import (
    OpenAIAudioTranscriptor,
)
from .shared.logger import get_logger

data_dir = "../data"



load_dotenv(override=True)

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def main():
    parser = argparse.ArgumentParser(description="Audio Embedder CLI")
    parser.add_argument(
        "--episodes-file",
        default=os.path.join(data_dir, "episodes.json"),
        help="Path to episodes.json file",
    )
    parser.add_argument(
        "--transcriptions-dir",
        default=os.path.join(data_dir, "transcriptions"),
        help="Directory to store transcriptions",
    )
    parser.add_argument(
        "--embeddings-dir",
        default="../data/embeddings",
        help="Directory to store embeddings",
    )
    parser.add_argument(
        "--command",
        choices=["process", "search"],
        default="process",
        help="Command to execute",
    )
    parser.add_argument("--query", help="Search query (required for search command)")
    parser.add_argument(
        "--top-k", type=int, default=10, help="Number of results to return for search"
    )
    parser.add_argument(
        "--transcriptor",
        choices=["mock", "openai"],
        default="mock",
        help="Transcriptor to use (mock or openai)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (process only first episode, no data saved)",
    )

    args = parser.parse_args()

    logger = get_logger(__name__)

    episode_repository = JSONEpisodeRepository(args.episodes_file)
    transcription_repository = FileTranscriptionRepository(args.transcriptions_dir)
    embedding_repository = MockEmbeddingRepository(args.embeddings_dir)

    if args.transcriptor == "openai":
        audio_transcriptor = OpenAIAudioTranscriptor()
        logger.info("Using OpenAI transcriptor")
    else:
        audio_transcriptor = MockAudioTranscriptor()
        logger.info("Using mock transcriptor")

    embedding_service = MockEmbeddingService()

    if args.command == "process":
        if args.dry_run:
            logger.info("🧪 Starting episode processing in DRY RUN mode...")
        else:
            logger.info("Starting episode processing...")

        use_case = ProcessEpisodesUseCase(
            episode_repository,
            transcription_repository,
            embedding_repository,
            audio_transcriptor,
            embedding_service,
        )
        use_case.execute(dry_run=args.dry_run)

        if args.dry_run:
            logger.info("🧪 DRY RUN episode processing completed.")
        else:
            logger.info("Episode processing completed.")

    elif args.command == "search":
        if not args.query:
            logger.error("Query is required for search command")
            return

        logger.info(f"Searching for: {args.query}")
        use_case = SearchEpisodesUseCase(embedding_repository, embedding_service)
        results = use_case.execute(args.query, args.top_k)

        for i, result in enumerate(results, 1):
            logger.info(f"Result {i}: {result.chunk_text[:100]}...")


if __name__ == "__main__":
    main()
