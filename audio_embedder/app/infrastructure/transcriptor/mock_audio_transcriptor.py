from typing import Optional
from datetime import datetime
from ...domain.entities.episode import Episode
from ...domain.entities.transcription import Transcription
from ...application.services.audio_transcriptor import AudioTranscriptor


class MockAudioTranscriptor(AudioTranscriptor):
    def transcribe(self, episode: Episode) -> Optional[Transcription]:
        return Transcription(
            episode_id=episode.url,
            text=f"Mock transcription for episode: {episode.title}",
            language="es",
            created_at=datetime.now(),
            duration=episode.duration,
            file_path=None,
            confidence_score=0.95
        )