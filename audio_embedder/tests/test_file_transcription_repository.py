import json
import os
import tempfile
import unittest
from datetime import datetime

from app.domain.entities.transcription import Transcription
from app.infrastructure.repositories.file_transcription_repository import (
    FileTranscriptionRepository,
)


class TestFileTranscriptionRepository(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repository = FileTranscriptionRepository(self.temp_dir)
        
    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_save_new_transcription_creates_file(self):
        transcription = Transcription(
            episode_id="test_episode_1",
            text="Test transcription text",
            language="es",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            duration=900,
            file_path="/test/path.mp3",
        )

        result = self.repository.save(transcription)

        self.assertEqual(result.episode_id, transcription.episode_id)
        self.assertEqual(result.text, transcription.text)
        
        # Verify file was created
        file_path = os.path.join(self.temp_dir, "test_episode_1.json")
        self.assertTrue(os.path.exists(file_path))

    def test_save_existing_transcription_does_not_overwrite(self):
        # Create initial transcription
        original_transcription = Transcription(
            episode_id="test_episode_2",
            text="Original transcription text",
            language="es",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            duration=900,
            file_path="/original/path.mp3",
        )
        
        # Save original
        self.repository.save(original_transcription)
        
        # Try to save different transcription with same episode_id
        new_transcription = Transcription(
            episode_id="test_episode_2",
            text="NEW transcription text - this should not be saved",
            language="en",
            created_at=datetime(2023, 2, 1, 12, 0, 0),
            duration=1200,
            file_path="/new/path.mp3",
        )
        
        # This should return the original transcription, not save the new one
        result = self.repository.save(new_transcription)
        
        # Result should be the original transcription, not the new one
        self.assertEqual(result.text, "Original transcription text")
        self.assertEqual(result.language, "es")
        self.assertEqual(result.duration, 900)
        self.assertEqual(result.file_path, "/original/path.mp3")
        
        # Verify file content hasn't changed
        file_path = os.path.join(self.temp_dir, "test_episode_2.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["text"], "Original transcription text")
            self.assertEqual(data["language"], "es")

    def test_get_by_episode_id_returns_existing_transcription(self):
        transcription = Transcription(
            episode_id="test_episode_3",
            text="Test get transcription",
            language="es",
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            duration=900,
        )
        
        # Save transcription
        self.repository.save(transcription)
        
        # Retrieve it
        result = self.repository.get_by_episode_id("test_episode_3")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.episode_id, "test_episode_3")
        self.assertEqual(result.text, "Test get transcription")

    def test_get_by_episode_id_returns_none_for_nonexistent(self):
        result = self.repository.get_by_episode_id("nonexistent_episode")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()