# Scraping Tool

## Overview

This FastAPI application provides an endpoint to scrape product data from [Dental Stall](https://dentalstall.com/shop/). The scraper collects product names, prices, and images, and stores the data in a JSON file. The tool supports optional settings for limiting the number of pages to scrape and using a proxy. Authentication is required to access the scraping endpoint using a static token.

## Features

- **Scrape Product Data**: Collects product name, price, and image URL.
- **Limit Pages**: Optionally limit the number of pages to scrape.
- **Proxy Support**: Optionally use a proxy for scraping.
- **Authentication**: Access the API using a static token.
- **Data Storage**: Saves scraped data to a local JSON file.
- **Progress Notification**: Provides progress updates after each page and at the end of the scraping process.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a Virtual Environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Update `settings.py`**:

    - Set the `API_TOKEN` to a secure token of your choice.
    - Configure other settings as needed (e.g., `BASE_URL`, `IMAGE_DIR`, `DB_PATH`).

## Usage

1. **Start the FastAPI Server**:

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Scrape Data**:

    - **Endpoint**: `/scrape`
    - **Method**: GET
    - **Parameters**:
        - `limit` (optional): Limit the number of pages to scrape.
        - `proxy` (optional): Provide a proxy string.
    
    **Example cURL Command**:

    ```bash
    curl -X GET "http://127.0.0.1:8000/scrape?limit=5" -H "Authorization: Bearer static_token"
    ```

    **Example using Python `requests`**:

    ```python
    import requests

    headers = {
        "Authorization": "Bearer static_token"
    }
    response = requests.get("http://127.0.0.1:8000/scrape?limit=5", headers=headers)
    print(response.json())
    ```

## Token Configuration

The static API token is stored in `app/settings.py`. Update the `API_TOKEN` variable with your desired token:

```python
# app/settings.py
API_TOKEN = "static_token"
```

## Data Storage

Scraped data is saved to a JSON file specified in settings.py:

```python
# app/settings.py
DB_PATH = "scraped_data.json"
```

Ensure that the directory for saving images exists and is writable:
```python
# app/settings.py
IMAGE_DIR = "images/"
```

## Progress Notifications

- **Progress Updates**: Printed to the console after scraping each page.
- **Final Notification**: Displays the total number of products scraped and saved at the end of the scraping process.
