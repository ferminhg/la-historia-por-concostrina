"""
Tests para el módulo principal
"""
import pytest
from unittest.mock import patch
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main


class TestMain:
    """Tests para la función main"""
    
    @patch('builtins.print')
    def test_main_prints_hello_world(self, mock_print):
        """Test que verifica que main imprime 'Hola mundo'"""
        result = main()
        
        mock_print.assert_called_once_with("¡Hola mundo desde Podcast Crawler!")
        assert result == 0
    
    @patch('sys.argv', ['main.py', '--version'])
    @patch('argparse.ArgumentParser.exit')
    def test_main_with_version_flag(self, mock_exit):
        """Test que verifica el flag --version"""
        main()
        mock_exit.assert_called_once() 