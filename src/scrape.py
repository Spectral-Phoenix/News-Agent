import json
import logging
import re
import time
from datetime import datetime

import newspaper
import requests
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)

def extract_date(link):
    """Extracts the date from a URL."""
    match = re.search(r"/(\d{4}/\d{2}/\d{2})/", link)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%Y/%m/%d").date()
    else:
        return None

def scrape_links(category_url, category):
    """Scrapes links from a specified category URL."""
    try:
        resp = requests.get(category_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        return [(a['href'], category) for a in soup.select('h2 a')]
    except requests.exceptions.RequestException as req_exc:
        logging.error(f"Error scraping {category_url}: {req_exc}")
        return []

def parse_article(link):
    """Parses article content from a URL using newspaper3k."""
    try:
        article = newspaper.Article(link)
        article.download()
        article.parse()

        if article.title and article.text:
            return {
                "title": article.title,
                "content": article.text,
                "image_links": article.top_image,
                "link": link,
            }
        else:
            logging.error(f"Error parsing article content for {link}: Title or content not found.")
            return None

    except newspaper.article.ArticleException as article_exc:
        logging.error(f"Error fetching or parsing article content for {link}: {article_exc}")
        return None

    except Exception as e:
        logging.error(f"Error parsing article content for {link}: {e}")
        return None

def scrape_articles(date_input):
    """Scrapes articles from TechCrunch for a specific date."""
    if not date_input:
        logging.error("Please provide a valid date.")
        return

    try:
        target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Config
    BASE_URL = "https://techcrunch.com/category/"
    CATEGORIES = ["artificial-intelligence", "apps", "biotech-health", "climate", "commerce",
                  "enterprise", "fintech", "gadgets", "gaming", "government-policy", "hardware",
                  "media-entertainment", "privacy", "robotics", "security", "social", "space",
                  "startups", "transportation", "venture"]

    logging.info("Fetching articles...")

    start_time = time.time()
    links = set() 

    for category in CATEGORIES:
        category_url = BASE_URL + category + "/"
        category_links = scrape_links(category_url, category)

        for link, _ in category_links:
            date = extract_date(link)
            if date == target_date:
                links.add(link)

    articles = []

    for link in links:
        article = parse_article(link)
        if article:
            articles.append(article)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_in_seconds = int(elapsed_time)

    data = {
        "source": "TechCrunch",
        "date": str(target_date),
        "no_of_articles": len(articles),
        "articles": articles
    }

    logging.info(f"{len(articles)} articles scraped successfully!")
    logging.info(f"Elapsed time: {elapsed_time_in_seconds} seconds")
    return data

# Example Usage (Commented out)
# if __name__ == "__main__":
#    date_input = input("Enter the date (YYYY-MM-DD): ")
#    data = scrape_articles(date_input)
#    print(data)