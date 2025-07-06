from datetime import datetime
from typing import Optional

from ...application.services.audio_transcriptor import AudioTranscriptor
from ...domain.entities.episode import Episode
from ...domain.entities.transcription import Transcription


class MockAudioTranscriptor(AudioTranscriptor):
    def transcribe(self, episode: Episode) -> Optional[Transcription]:
        return Transcription(
            episode_id=episode.id,
            text=f"Mock transcription for episode: {episode.title}",
            language="es",
            created_at=datetime.now(),
            duration=episode.duration,
            file_path=None,
        )
