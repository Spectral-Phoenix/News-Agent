import json
import logging
import re
from datetime import date, datetime
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from newspaper import Article

# Configure logging
logging.basicConfig(filename='logs/tech_crunch_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def extract_date_from_link(link: str) -> Optional[date]:

    match = re.search(r"/(\d{4}/\d{2}/\d{2})/", link)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%Y/%m/%d").date()
    else:
        return None

def scrape_category_links(category_url: str) -> list[str]:

    try:
        resp = requests.get(category_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        return [a['href'] for a in soup.select('h2 a')]
    except requests.exceptions.RequestException as req_exc:
        logging.error(f"Error scraping {category_url}: {req_exc}")
        return []

def scrape_article_content(link: str) -> Optional[Dict[str, str]]:

    try:
        article = Article(link, language='en')
        article.download()
        article.parse()
        article_date = article.publish_date.date()
        if article_date == str(date.today()):
            return {
                'title': article.title,
                'publish_date': article.publish_date.strftime('%Y-%m-%d'),
                'text': article.text,
                'url': link,
            }
    except Exception as exc:
        logging.error(f"Unexpected error occurred while scraping {link}: {exc}")
    return None

BASE_URL = "https://techcrunch.com/category/"
CATEGORIES = [
    "artificial-intelligence", "apps", "biotech-health", "climate", "commerce", "enterprise",
    "fintech", "gadgets", "gaming", "government-policy", "hardware", "media-entertainment",
    "privacy", "robotics", "security", "social", "space", "startups", "transportation", "venture"
]

def main():

    logging.info("Scraping Started")
    today_links = set()

    # Scrape links from all categories
    for category in CATEGORIES:
        category_url = BASE_URL + category + "/"
        category_links = scrape_category_links(category_url)
        for link in category_links:
            article_date = extract_date_from_link(link)
            if str(article_date) == str(date.today()):
                today_links.add(link)

    # Scrape article content for today's links
    data = {"source": "tech-crunch", "articles": []}
    for i, link in enumerate(today_links):
        logging.info(f"Scraping {i + 1} out of {len(today_links)}")
        article_data = scrape_article_content(link)
        if article_data:
            data["articles"].append(article_data)

    # Save data to a JSON file
    today_str = str(date.today())
    file_path = f"data/tech_crunch/{today_str}_tech_crunch.json"
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

    logging.info("Scraping Completed")

if __name__ == "__main__":
    main()