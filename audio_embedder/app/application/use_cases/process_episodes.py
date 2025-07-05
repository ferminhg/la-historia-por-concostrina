from typing import List
from ...domain.repositories.episode_repository import EpisodeRepository
from ...domain.repositories.transcription_repository import TranscriptionRepository
from ...domain.repositories.embedding_repository import EmbeddingRepository
from ..services.audio_transcriptor import AudioTranscriptor
from ..services.embedding_service import EmbeddingService


class ProcessEpisodesUseCase:
    def __init__(
        self,
        episode_repository: EpisodeRepository,
        transcription_repository: TranscriptionRepository,
        embedding_repository: EmbeddingRepository,
        audio_transcriptor: AudioTranscriptor,
        embedding_service: EmbeddingService
    ):
        self.episode_repository = episode_repository
        self.transcription_repository = transcription_repository
        self.embedding_repository = embedding_repository
        self.audio_transcriptor = audio_transcriptor
        self.embedding_service = embedding_service
    
    def execute(self) -> None:
        episodes = self.episode_repository.get_all()
        
        for episode in episodes:
            existing_transcription = self.transcription_repository.get_by_episode_id(episode.url)
            
            if existing_transcription:
                continue
            
            transcription = self.audio_transcriptor.transcribe(episode)
            if not transcription:
                continue
            
            saved_transcription = self.transcription_repository.save(transcription)
            
            embeddings = self.embedding_service.create_embeddings(saved_transcription)
            
            self.embedding_repository.save_batch(embeddings)