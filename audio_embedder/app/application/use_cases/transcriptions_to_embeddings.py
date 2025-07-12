import os
from pathlib import Path
from typing import List, Dict, Any

from ...domain.repositories.embedding_repository import EmbeddingRepository
from ...domain.repositories.transcription_repository import TranscriptionRepository
from ...shared.logger import get_logger
from ...shared.semantic_chunker import SemanticChunker
from ..services.embedding_service import EmbeddingService


class TranscriptionsToEmbeddingsUseCase:
    def __init__(
        self,
        transcription_repository: TranscriptionRepository,
        embedding_repository: EmbeddingRepository,
        embedding_service: EmbeddingService,
        use_supabase: bool = False,
    ):
        self.transcription_repository = transcription_repository
        self.embedding_repository = embedding_repository
        self.embedding_service = embedding_service
        self.use_supabase = use_supabase
        self.logger = get_logger(self.__class__.__name__)
        self.chunker = SemanticChunker()

    def extract_episode_metadata(self, transcription) -> Dict[str, Any]:
        """Extrae metadatos del episodio desde la transcripción"""
        return {
            "episode_id": transcription.episode_id,
            "title": getattr(transcription, 'title', transcription.episode_id),
            "duration": getattr(transcription, 'duration', 0),
            "language": getattr(transcription, 'language', 'es'),
            "file_path": getattr(transcription, 'file_path', ''),
        }

    def process_with_semantic_chunking(self, transcription, dry_run: bool = False) -> List:
        """Procesa transcripción usando chunking semántico mejorado"""
        try:
            episode_metadata = self.extract_episode_metadata(transcription)
            chunks = self.chunker.chunk_transcript(transcription.text, episode_metadata)
            
            if not chunks:
                self.logger.warning(f"No chunks generated for {transcription.episode_id}")
                return []
            
            self.logger.info(f"Generated {len(chunks)} semantic chunks for {transcription.episode_id}")
            
            if dry_run:
                self.logger.info(f"DRY RUN: Would process {len(chunks)} chunks")
                return []
            
            # Si usa Supabase, el servicio maneja el almacenamiento directamente
            if self.use_supabase and hasattr(self.embedding_service, 'create_embeddings'):
                return self.embedding_service.create_embeddings(transcription)
            
            # Para servicios tradicionales, usar el método existente
            return self.embedding_service.create_embeddings(transcription)
            
        except Exception as e:
            self.logger.error(f"Error processing transcription {transcription.episode_id}: {str(e)}")
            return []

    def execute(self, dry_run: bool = False) -> None:
        transcriptions = self.transcription_repository.get_all()
        
        if not transcriptions:
            self.logger.warning("No transcriptions found to process")
            return

        if dry_run:
            import random
            self.logger.info("🧪 DRY RUN MODE: Processing a random transcription")
            transcriptions = [random.choice(transcriptions)]

        total_transcriptions = len(transcriptions)
        self.logger.info(
            f"Processing embeddings for {total_transcriptions} transcription{'s' if total_transcriptions != 1 else ''}"
        )

        for i, transcription in enumerate(transcriptions, 1):
            self.logger.info(f"[{i}/{total_transcriptions}] Processing: {transcription.episode_id}")

            # Skip if embeddings already exist (only for non-Supabase services)
            if not self.use_supabase:
                existing_embeddings = self.embedding_repository.get_by_episode_id(
                    transcription.episode_id
                )

                if existing_embeddings:
                    self.logger.info(
                        f"[{i}/{total_transcriptions}] Skipping - embeddings already exist"
                    )
                    continue

            # Process with semantic chunking
            embeddings = self.process_with_semantic_chunking(transcription, dry_run)
            
            if not embeddings and not dry_run:
                self.logger.warning(
                    f"[{i}/{total_transcriptions}] Failed to create embeddings"
                )
                continue

            # Save to local repository only if not using Supabase
            if not self.use_supabase and embeddings and not dry_run:
                self.embedding_repository.save_batch(embeddings)
                self.logger.info(f"[{i}/{total_transcriptions}] Embeddings created and saved to local repository")
            elif not dry_run:
                self.logger.info(f"[{i}/{total_transcriptions}] Embeddings created and saved to Supabase")

        if dry_run:
            self.logger.info("🧪 DRY RUN completed - no embeddings were saved")
        else:
            self.logger.info("✅ Transcriptions to embeddings processing completed")