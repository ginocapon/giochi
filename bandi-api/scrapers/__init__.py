# Scrapers API-First
from .bandi_statici import scrape_bandi_statici
from .api_rss import scrape_rss_feeds
from .api_opendata import scrape_opendata
from .api_anac import scrape_anac
from .api_contratti import scrape_contratti_pubblici

__all__ = [
    'scrape_bandi_statici',
    'scrape_rss_feeds',
    'scrape_opendata',
    'scrape_anac',
    'scrape_contratti_pubblici'
]
