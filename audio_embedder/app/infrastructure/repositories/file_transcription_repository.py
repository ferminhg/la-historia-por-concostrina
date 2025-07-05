import json
import os
from typing import List, Optional
from datetime import datetime
from ...domain.repositories.transcription_repository import TranscriptionRepository
from ...domain.entities.transcription import Transcription


class FileTranscriptionRepository(TranscriptionRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def get_by_episode_id(self, episode_id: str) -> Optional[Transcription]:
        file_path = self._get_file_path(episode_id)
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return self._dict_to_transcription(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def save(self, transcription: Transcription) -> Transcription:
        file_path = self._get_file_path(transcription.episode_id)
        data = self._transcription_to_dict(transcription)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        return transcription
    
    def get_all(self) -> List[Transcription]:
        transcriptions = []
        for filename in os.listdir(self.base_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.base_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        transcriptions.append(self._dict_to_transcription(data))
                except (json.JSONDecodeError, KeyError):
                    continue
        return transcriptions
    
    def _get_file_path(self, episode_id: str) -> str:
        filename = f"{hash(episode_id)}.json"
        return os.path.join(self.base_path, filename)
    
    def _dict_to_transcription(self, data: dict) -> Transcription:
        return Transcription(
            episode_id=data['episode_id'],
            text=data['text'],
            language=data['language'],
            created_at=datetime.fromisoformat(data['created_at']),
            duration=data['duration'],
            file_path=data.get('file_path'),
            confidence_score=data.get('confidence_score')
        )
    
    def _transcription_to_dict(self, transcription: Transcription) -> dict:
        return {
            'episode_id': transcription.episode_id,
            'text': transcription.text,
            'language': transcription.language,
            'created_at': transcription.created_at.isoformat(),
            'duration': transcription.duration,
            'file_path': transcription.file_path,
            'confidence_score': transcription.confidence_score
        }