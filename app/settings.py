from pathlib import Path

class Settings:
    BASE_URL = "https://dentalstall.com/shop"
    IMAGE_DIR = Path("images/")
    DB_PATH = Path("scraped_data.json")
    API_TOKEN = "static_token"

    def __init__(self):
        self.IMAGE_DIR.mkdir(exist_ok=True)

settings = Settings()

