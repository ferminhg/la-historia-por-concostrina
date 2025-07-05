import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.use_cases.crawl_podcast import CrawlPodcastUseCase
from infrastructure.repositories.hardcoded_rss_url_repository import HardcodedRSSUrlRepository
from shared.logger import get_logger

logger = get_logger(__name__)

data_dir = os.path.join(os.path.dirname(__file__), "../../data")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Podcast Crawler - Herramienta para hacer crawling de podcasts de Nieves Concostrina"
    )
    parser.add_argument("--version", action="version", version="podcast-crawler 1.0.0")

    args = parser.parse_args()

    logger.info("👋 Hi from Podcast Crawler! 🐛")
    
    rss_url_repository = HardcodedRSSUrlRepository(data_dir=data_dir)
    usecase = CrawlPodcastUseCase(rss_url_repository)
    
    podcasts = usecase.execute()
    
    logger.info(f"✅ Se obtuvieron {len(podcasts)} podcasts exitosamente")

    return 0


if __name__ == "__main__":
    sys.exit(main())
