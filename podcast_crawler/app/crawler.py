import sys
import argparse
from typing import Optional

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Función principal del programa
    """
    parser = argparse.ArgumentParser(
        description="Podcast Crawler - Herramienta para hacer crawling de podcasts de Nieves Concostrina"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="podcast-crawler 1.0.0"
    )
    
    args = parser.parse_args()
    
    logger.info("¡Hola mundo desde Podcast Crawler!")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
