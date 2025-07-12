import argparse
import os
from dotenv import load_dotenv

from .application.use_cases.process_episodes import ProcessEpisodesUseCase
from .application.use_cases.search_episodes import SearchEpisodesUseCase
from .application.use_cases.transcriptions_to_embeddings import TranscriptionsToEmbeddingsUseCase
from .application.use_cases.search_supabase import SearchSupabaseUseCase
from .infrastructure.embedder.mock_embedding_service import MockEmbeddingService
from .infrastructure.embedder.supabase_embedding_service import SupabaseEmbeddingService
from .infrastructure.repositories.file_transcription_repository import (
    FileTranscriptionRepository,
)
from .infrastructure.repositories.json_episode_repository import JSONEpisodeRepository
from .infrastructure.repositories.mock_embedding_repository import (
    MockEmbeddingRepository,
)
from .infrastructure.repositories.file_cost_repository import FileCostRepository
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
        "--costs-dir",
        default=os.path.join(data_dir, "costs"),
        help="Directory to store cost tracking data",
    )
    parser.add_argument(
        "--command",
        choices=["process", "search", "transcriptions-to-embeddings", "search-supabase"],
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
    parser.add_argument(
        "--use-supabase",
        action="store_true",
        help="Use Supabase for embeddings storage (requires SUPABASE_URL and SUPABASE_KEY)",
    )
    parser.add_argument(
        "--episode-id",
        help="Filter search by specific episode ID (for search-supabase command)",
    )
    parser.add_argument(
        "--show-summary",
        action="store_true",
        help="Show episode summary instead of search (for search-supabase command)",
    )

    args = parser.parse_args()

    logger = get_logger(__name__)

    episode_repository = JSONEpisodeRepository(args.episodes_file)
    transcription_repository = FileTranscriptionRepository(args.transcriptions_dir)
    embedding_repository = MockEmbeddingRepository(args.embeddings_dir)
    cost_repository = FileCostRepository(args.costs_dir)

    if args.transcriptor == "openai":
        audio_transcriptor = OpenAIAudioTranscriptor(cost_repository=cost_repository)
        logger.info("Using OpenAI transcriptor with cost tracking")
    else:
        audio_transcriptor = MockAudioTranscriptor()
        logger.info("Using mock transcriptor")

    # Configure embedding service
    if args.use_supabase:
        try:
            embedding_service = SupabaseEmbeddingService()
            logger.info("Using Supabase embedding service")
        except ValueError as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            logger.info("Falling back to mock embedding service")
            embedding_service = MockEmbeddingService()
    else:
        embedding_service = MockEmbeddingService()
        logger.info("Using mock embedding service")

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
            cost_repository if args.transcriptor == "openai" else None,
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

    elif args.command == "transcriptions-to-embeddings":
        if args.dry_run:
            logger.info("🧪 Starting transcriptions to embeddings processing in DRY RUN mode...")
        else:
            logger.info("Starting transcriptions to embeddings processing...")

        use_case = TranscriptionsToEmbeddingsUseCase(
            transcription_repository,
            embedding_repository,
            embedding_service,
            use_supabase=args.use_supabase,
        )
        use_case.execute(dry_run=args.dry_run)

        if args.dry_run:
            logger.info("🧪 DRY RUN transcriptions to embeddings processing completed.")
        else:
            logger.info("Transcriptions to embeddings processing completed.")

    elif args.command == "search-supabase":
        try:
            search_use_case = SearchSupabaseUseCase()
            
            # Mostrar resumen del episodio si se solicita
            if args.show_summary and args.episode_id:
                logger.info(f"📊 Obteniendo resumen del episodio: {args.episode_id}")
                summary = search_use_case.get_episode_summary(args.episode_id)
                
                logger.info("=" * 60)
                logger.info(f"📋 RESUMEN DEL EPISODIO: {summary['episode_id']}")
                logger.info("=" * 60)
                logger.info(f"🎙️  Título: {summary.get('title', 'N/A')}")
                logger.info(f"📄 Total chunks: {summary.get('chunks_count', 0)}")
                logger.info(f"📝 Total palabras: {summary.get('total_words', 0)}")
                logger.info(f"⏱️  Duración estimada: {summary.get('duration_minutes', 0)} minutos")
                logger.info(f"📊 Promedio palabras/chunk: {summary.get('avg_chunk_words', 0):.1f}")
                
                chunk_types = summary.get('chunk_types', {})
                if chunk_types:
                    logger.info("🏷️  Tipos de chunks:")
                    for chunk_type, count in chunk_types.items():
                        logger.info(f"   - {chunk_type}: {count}")
                logger.info("=" * 60)
                
            else:
                # Realizar búsqueda normal
                if not args.query:
                    logger.error("❌ Query es requerido para el comando search-supabase")
                    return
                
                logger.info(f"🔍 Buscando en Supabase: '{args.query}'")
                
                if args.episode_id:
                    logger.info(f"🎯 Filtrando por episodio: {args.episode_id}")
                    results = search_use_case.search_by_episode(args.query, args.episode_id, args.top_k)
                else:
                    results = search_use_case.execute(args.query, args.top_k)
                
                if not results:
                    logger.warning("❌ No se encontraron resultados")
                    return
                
                logger.info("=" * 80)
                logger.info(f"🔍 RESULTADOS DE BÚSQUEDA PARA: '{args.query}'")
                logger.info("=" * 80)
                
                for result in results:
                    logger.info(f"\n🏆 RESULTADO #{result['rank']}")
                    logger.info(f"🎙️  Episodio: {result['episode_id']} - {result['title']}")
                    logger.info(f"🏷️  Tipo: {result['chunk_type']}")
                    logger.info(f"⏱️  Timestamp: ~{result['estimated_timestamp_minutes']:.1f} min")
                    logger.info(f"📝 Contenido:")
                    
                    # Formatear contenido con mejor legibilidad
                    content = result['content']
                    if len(content) > 500:
                        content = content[:500] + "..."
                    
                    # Dividir en líneas de máximo 80 caracteres
                    words = content.split()
                    lines = []
                    current_line = ""
                    
                    for word in words:
                        if len(current_line + " " + word) <= 76:  # 80 - 4 espacios de indentación
                            current_line += " " + word if current_line else word
                        else:
                            if current_line:
                                lines.append("    " + current_line)
                                current_line = word
                            else:
                                lines.append("    " + word)
                    
                    if current_line:
                        lines.append("    " + current_line)
                    
                    logger.info("\n".join(lines))
                    logger.info("-" * 80)
                
                logger.info(f"\n✅ Búsqueda completada. {len(results)} resultados encontrados.")
                
        except ValueError as e:
            logger.error(f"❌ Error de configuración: {e}")
            logger.error("💡 Asegúrate de que SUPABASE_URL y SUPABASE_KEY estén configurados")
        except Exception as e:
            logger.error(f"❌ Error en búsqueda Supabase: {str(e)}")

if __name__ == "__main__":
    main()
