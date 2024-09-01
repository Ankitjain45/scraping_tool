import requests
import json
import time
from bs4 import BeautifulSoup
from app.settings import settings
from app.cache import Cache
from pathlib import Path


class Scraper:
    def __init__(self, base_url, limit=None, proxy=None):
        self.base_url = base_url
        self.limit = limit
        self.proxy = proxy
        self.scraped_data = []
        self.total_products = []
        self.cache = Cache()

    def fetch_page(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        retries = 3

        for _ in range(retries):
            try:
                response = requests.get(url, headers=headers, proxies=proxies)
                if response.status_code == 200:
                    return response.content
            except requests.exceptions.RequestException:
                time.sleep(3)
        return None

    @staticmethod
    def parse_product(product):
        # Get product name
        product_name_element = product.select_one("h2.woo-loop-product__title")
        product_name = (
            product_name_element.get_text(strip=True) if product_name_element else str()
        )

        # Get product price
        price_element = product.select_one(
            "span.price ins .woocommerce-Price-amount bdi"
        )
        if not price_element:
            price_element = product.select_one(
                "span.price .woocommerce-Price-amount bdi"
            )

        product_price = 0.0
        if price_element:
            price_text = price_element.get_text(strip=True).replace(",", "")
            # Remove non-numeric characters (except for the decimal point)
            product_price = float(
                "".join(filter(lambda x: x.isdigit() or x == ".", price_text))
            )

        # Get image URL
        image_element = product.select_one("div.mf-product-thumbnail a img")
        image_url = (
            image_element["data-lazy-src"]
            if image_element and image_element.has_attr("data-lazy-src")
            else None
        )
        if not image_url:
            image_url = (
                image_element["src"]
                if image_element and image_element.has_attr("src")
                else None
            )

        image_path = None
        if image_url:
            image_name = Path(image_url).name
            image_path = settings.IMAGE_DIR / image_name

            # Download and save image
            img_data = requests.get(image_url).content
            with open(image_path, "wb") as handler:
                handler.write(img_data)

        return {
            "product_title": product_name,
            "product_price": product_price,
            "path_to_image": str(image_path) if image_path else str(),
        }

    def scrape_page(self, page):
        url = self.base_url if page == 1 else f"{self.base_url}/page/{page}/"
        page_content = self.fetch_page(url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, "html.parser")
        products = soup.select("ul.products.columns-4 li")
        return [self.parse_product(product) for product in products]

    def run(self):
        self.notify("Starting the scraping process...")
        page = 1
        while True:
            if self.limit and page > self.limit:
                break
            products = self.scrape_page(page)
            if not products:
                break

            for product in products:
                cached_price = self.cache.get(product["product_title"])
                if cached_price != product["product_price"]:
                    self.scraped_data.append(product)
                    self.cache.set(product["product_title"], product["product_price"])
                self.total_products.append(product)

            self.save_to_db()  # save data to db
            self.notify(
                message=f"Scraped {len(products)} products from page {page}."
            )
            page += 1

        self.notify(
            message=f"Scraping completed. total {len(self.total_products)} products scraped and {len(self.scraped_data)} products updated to db."
        )

    def save_to_db(self):
        # Save scraped data to a JSON file
        with open(settings.DB_PATH, "w") as f:
            json.dump(self.scraped_data, f, indent=4)

    @staticmethod
    def notify(message):
        print(message)
