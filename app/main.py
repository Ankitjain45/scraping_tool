from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.scraper import Scraper
from app.settings import settings

app = FastAPI()
security = HTTPBearer()


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials


@app.get("/")
def read_root():
    return {"message": "Welcome to the Scraping Tool"}


@app.get("/scrape", dependencies=[Depends(validate_token)])
def scrape(limit: int = None, proxy: str = None):
    scraper = Scraper(base_url=settings.BASE_URL, limit=limit, proxy=proxy)
    scraper.run()
    return {"message": f"Scraping completed. total {len(scraper.total_products)} products scraped and {len(scraper.scraped_data)} updated to db"}

