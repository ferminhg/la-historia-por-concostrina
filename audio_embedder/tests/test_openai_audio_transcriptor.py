import pytest
from unittest.mock import Mock, patch, mock_open
from datetime import datetime
from app.infrastructure.transcriptor.openai_audio_transcriptor import OpenAIAudioTranscriptor
from app.domain.entities.episode import Episode


class TestOpenAIAudioTranscriptor:
    @patch('app.infrastructure.transcriptor.openai_audio_transcriptor.OpenAI')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b"fake audio data")
    def test_transcribes_episode_successfully(self, mock_file, mock_exists, mock_openai_class):
        mock_exists.return_value = True
        
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_event1 = Mock()
        mock_event1.text = "Hello "
        mock_event2 = Mock()
        mock_event2.text = "world!"
        
        mock_stream = [mock_event1, mock_event2]
        mock_client.audio.transcriptions.create.return_value = mock_stream
        
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000,
            local_file_path="/path/to/test.mp3"
        )
        
        transcriptor = OpenAIAudioTranscriptor()
        result = transcriptor.transcribe(episode)
        
        assert result is not None
        assert result.episode_id == episode.url
        assert result.text == "Hello world!"
        assert result.language == "es"
        assert result.duration == episode.duration
        assert result.file_path == episode.local_file_path
        
        mock_client.audio.transcriptions.create.assert_called_once_with(
            file=mock_file.return_value,
            model="gpt-4o-mini-transcribe",
            stream=True,
            language="es"
        )
    
    @patch('os.path.exists')
    def test_returns_none_when_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000,
            local_file_path="/nonexistent/path.mp3"
        )
        
        transcriptor = OpenAIAudioTranscriptor()
        result = transcriptor.transcribe(episode)
        
        assert result is None
    
    def test_returns_none_when_no_local_file_path(self):
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000,
            local_file_path=None
        )
        
        transcriptor = OpenAIAudioTranscriptor()
        result = transcriptor.transcribe(episode)
        
        assert result is None
    
    @patch('app.infrastructure.transcriptor.openai_audio_transcriptor.OpenAI')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_handles_openai_api_error(self, mock_file, mock_exists, mock_openai_class):
        mock_exists.return_value = True
        
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.audio.transcriptions.create.side_effect = Exception("API Error")
        
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000,
            local_file_path="/path/to/test.mp3"
        )
        
        transcriptor = OpenAIAudioTranscriptor()
        result = transcriptor.transcribe(episode)
        
        assert result is None
    
    @patch('app.infrastructure.transcriptor.openai_audio_transcriptor.OpenAI')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_returns_none_for_empty_transcription(self, mock_file, mock_exists, mock_openai_class):
        mock_exists.return_value = True
        
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_event = Mock()
        mock_event.text = "   "
        mock_stream = [mock_event]
        mock_client.audio.transcriptions.create.return_value = mock_stream
        
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000,
            local_file_path="/path/to/test.mp3"
        )
        
        transcriptor = OpenAIAudioTranscriptor()
        result = transcriptor.transcribe(episode)
        
        assert result is None