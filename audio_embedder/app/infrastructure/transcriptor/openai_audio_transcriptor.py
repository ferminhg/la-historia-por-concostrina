import os
from datetime import datetime
from typing import Optional

from openai import OpenAI

from ...application.services.audio_transcriptor import AudioTranscriptor
from ...domain.entities.episode import Episode
from ...domain.entities.transcription import Transcription
from ...shared.logger import get_logger


class OpenAIAudioTranscriptor(AudioTranscriptor):
    def __init__(
        self, api_key: Optional[str] = None, model: str = "whisper-1"
    ):
        self.logger = get_logger(self.__class__.__name__)
        self.model = model

        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()

    def transcribe(self, episode: Episode) -> Optional[Transcription]:
        if not episode.local_file_path or not os.path.exists(episode.local_file_path):
            self.logger.error(f"Audio file not found: {episode.local_file_path}")
            return None

        try:
            self.logger.info(f"Starting transcription for episode: {episode.title}")

            with open(episode.local_file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    file=audio_file, 
                    model=self.model, 
                    language="es",
                    response_format="text"
                )

                transcription_text = response

                if not transcription_text.strip():
                    self.logger.warning(
                        f"Empty transcription for episode: {episode.title}"
                    )
                    return None

                transcription = Transcription(
                    episode_id=episode.id,
                    text=transcription_text.strip(),
                    language="es",
                    created_at=datetime.now(),
                    duration=episode.duration,
                    file_path=episode.local_file_path,
                )

                self.logger.info(
                    f"Successfully transcribed episode: {episode.title} "
                    f"({len(transcription_text)} characters)"
                )
                return transcription

        except Exception as e:
            self.logger.error(f"Error transcribing episode {episode.title}: {str(e)}")
            return None
