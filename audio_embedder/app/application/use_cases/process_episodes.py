from ...domain.repositories.embedding_repository import EmbeddingRepository
from ...domain.repositories.episode_repository import EpisodeRepository
from ...domain.repositories.transcription_repository import TranscriptionRepository
from ...shared.logger import get_logger
from ..services.audio_transcriptor import AudioTranscriptor
from ..services.embedding_service import EmbeddingService


class ProcessEpisodesUseCase:
    def __init__(
        self,
        episode_repository: EpisodeRepository,
        transcription_repository: TranscriptionRepository,
        embedding_repository: EmbeddingRepository,
        audio_transcriptor: AudioTranscriptor,
        embedding_service: EmbeddingService,
    ):
        self.episode_repository = episode_repository
        self.transcription_repository = transcription_repository
        self.embedding_repository = embedding_repository
        self.audio_transcriptor = audio_transcriptor
        self.embedding_service = embedding_service
        self.logger = get_logger(self.__class__.__name__)

    def execute(self, dry_run: bool = False) -> None:
        episodes = self.episode_repository.get_all()

        if dry_run:
            self.logger.info("🧪 DRY RUN MODE: Processing only the first episode")
            episodes = episodes[:1] if episodes else []

            if not episodes:
                self.logger.warning("No episodes found for dry run")
                return

        total_episodes = len(episodes)
        self.logger.info(
            f"Processing {total_episodes} episode{'s' if total_episodes != 1 else ''}"
        )

        for i, episode in enumerate(episodes, 1):
            self.logger.info(f"[{i}/{total_episodes}] Processing: {episode.title}")

            existing_transcription = self.transcription_repository.get_by_episode_id(
                episode.id
            )

            if existing_transcription:
                self.logger.info(
                    f"[{i}/{total_episodes}] Skipping - transcription already exists"
                )
                continue

            transcription = self.audio_transcriptor.transcribe(episode)
            if not transcription:
                self.logger.warning(
                    f"[{i}/{total_episodes}] Failed to transcribe episode"
                )
                continue

            if dry_run:
                self.logger.info(
                    f"[{i}/{total_episodes}] DRY RUN: Would save transcription"
                )
                self.logger.info(
                    f"[{i}/{total_episodes}] DRY RUN: Would create embeddings"
                )
            else:
                saved_transcription = self.transcription_repository.save(transcription)
                self.logger.info(f"[{i}/{total_episodes}] Transcription saved")

                embeddings = self.embedding_service.create_embeddings(
                    saved_transcription
                )
                self.embedding_repository.save_batch(embeddings)
                self.logger.info(f"[{i}/{total_episodes}] Embeddings created and saved")

        if dry_run:
            self.logger.info("🧪 DRY RUN completed - no data was actually saved")
