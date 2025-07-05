import os
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.logging.python_logger import PythonLogger
from shared.logger import get_logger


class TestPythonLogger:
    def test_creates_logger_with_name(self):
        logger = PythonLogger("test_logger")
        assert logger is not None

    @patch('logging.getLogger')
    def test_logs_info_message(self, mock_get_logger):
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_logger.handlers = []
        
        logger = PythonLogger("test")
        logger.info("test message")
        
        mock_logger.info.assert_called_once_with("test message")

    @patch('logging.getLogger')
    def test_logs_error_message(self, mock_get_logger):
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_logger.handlers = []
        
        logger = PythonLogger("test")
        logger.error("error message")
        
        mock_logger.error.assert_called_once_with("error message")


class TestLoggerFactory:
    def test_get_logger_returns_logger_instance(self):
        logger = get_logger("test")
        assert logger is not None

    def test_logger_has_all_methods(self):
        logger = get_logger("test")
        
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'critical')