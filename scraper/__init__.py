from .base import BaseScraper

# Try to import SNScrape, but make it optional for Python 3.13 compatibility
try:
    from .snscrape_client import SNScrapeScraper
    SNSCRAPE_AVAILABLE = True
except (ImportError, AttributeError) as e:
    SNScrapeScraper = None
    SNSCRAPE_AVAILABLE = False
    print(f"Warning: SNScrape not available: {e}")

from .twitter_api import TwitterAPIScraper
from .mock_scraper import MockScraper

__all__ = [
    "BaseScraper",
    "SNScrapeScraper",
    "TwitterAPIScraper",
    "MockScraper",
    "SNSCRAPE_AVAILABLE",
]
