from app.scraper import Scraper
from app.settings import settings


def test_scrape_data():
    scraper = Scraper(base_url=settings.BASE_URL, limit=1)
    scraper.run()
    assert len(scraper.total_products) > 0
    assert "product_title" in scraper.total_products[0]
    assert "product_price" in scraper.total_products[0]
    assert "path_to_image" in scraper.total_products[0]
