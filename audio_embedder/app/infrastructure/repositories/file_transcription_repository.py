import json
import os
from datetime import datetime
from typing import Optional

from ...domain.entities.transcription import Transcription
from ...domain.repositories.transcription_repository import TranscriptionRepository
from ...shared.logger import get_logger


class FileTranscriptionRepository(TranscriptionRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = get_logger(self.__class__.__name__)
        os.makedirs(base_path, exist_ok=True)

    def get_by_episode_id(self, episode_id: str) -> Optional[Transcription]:
        file_path = self._get_file_path(episode_id)
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, encoding="utf-8") as file:
                data = json.load(file)
                return self._dict_to_transcription(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save(self, transcription: Transcription) -> Transcription:
        file_path = self._get_file_path(transcription.episode_id)
        
        # Check if file already exists
        if os.path.exists(file_path):
            self.logger.info(
                f"Transcription file already exists for episode {transcription.episode_id}, "
                f"skipping save to preserve existing data"
            )
            # Return the existing transcription instead of overwriting
            existing_transcription = self.get_by_episode_id(transcription.episode_id)
            if existing_transcription:
                return existing_transcription
            else:
                # Fallback if file exists but couldn't be read
                self.logger.warning(
                    f"Could not read existing transcription file for episode {transcription.episode_id}, "
                    f"returning new transcription without saving"
                )
                return transcription
        
        # File doesn't exist, safe to create new one
        data = self._transcription_to_dict(transcription)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Transcription saved for episode {transcription.episode_id}")
        return transcription

    def get_all(self) -> list[Transcription]:
        transcriptions = []
        for filename in os.listdir(self.base_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.base_path, filename)
                try:
                    with open(file_path, encoding="utf-8") as file:
                        data = json.load(file)
                        transcriptions.append(self._dict_to_transcription(data))
                except (json.JSONDecodeError, KeyError):
                    continue
        return transcriptions

    def _get_file_path(self, episode_id: str) -> str:
        filename = f"{episode_id}.json"
        return os.path.join(self.base_path, filename)

    def _dict_to_transcription(self, data: dict) -> Transcription:
        return Transcription(
            episode_id=data["episode_id"],
            text=data["text"],
            language=data["language"],
            created_at=datetime.fromisoformat(data["created_at"]),
            duration=data["duration"],
            file_path=data.get("file_path"),
        )

    def _transcription_to_dict(self, transcription: Transcription) -> dict:
        return {
            "episode_id": transcription.episode_id,
            "text": transcription.text,
            "language": transcription.language,
            "created_at": transcription.created_at.isoformat(),
            "duration": transcription.duration,
            "file_path": transcription.file_path,
        }
