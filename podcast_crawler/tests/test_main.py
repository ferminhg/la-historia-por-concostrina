import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.crawler import main


class TestMain:
    @patch("sys.argv", ["app.crawler"])
    @patch("builtins.print")
    def test_main_prints_hello_world(self, mock_print):
        result = main()
        assert result == 0

    @patch("sys.argv", ["main.py", "--version"])
    @patch("argparse.ArgumentParser.exit")
    def test_main_with_version_flag(self, mock_exit):
        main()
        mock_exit.assert_called_once()
