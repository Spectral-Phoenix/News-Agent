import json
import logging
import newspaper
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)

def extract_date(link):
    """
    Extract the date from a URL.

    Parameters:
        link (str): URL string.

    Returns:
        datetime.date or None: Extracted date or None if not found.
    """
    match = re.search(r"/(\d{4}/\d{2}/\d{2})/", link)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%Y/%m/%d").date()
    else:
        return None

def scrape_links(category_url, category):
    """
    Scrape links from a specified category URL.

    Parameters:
        category_url (str): URL of the category.
        category (str): Category name.

    Returns:
        list: List of tuples containing (link, category).
    """
    try:
        resp = requests.get(category_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        return [(a['href'], category) for a in soup.select('h2 a')]
    except requests.exceptions.RequestException as req_exc:
        logging.error(f"Error scraping {category_url}: {req_exc}")
        return []


def parse_article(link):
    """
    Parse article content from a specified article URL using newspaper3k.

    Parameters:
        link (str): URL of the article.

    Returns:
        dict or None: Parsed article data or None if parsing fails.
    """
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
    """
    Scrape articles from TechCrunch based on a specified date.

    Parameters:
        date_input (str): Target date in the format 'YYYY-MM-DD'.

    Returns:
        bytes or None: JSON data in bytes or None if errors occur during the process.
    """
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
    links = set()  # Set to store unique links

    for category in CATEGORIES:
        category_url = BASE_URL + category + "/"
        category_links = scrape_links(category_url, category)

        for link, category in category_links:
            date = extract_date(link)

            if date == target_date:
                links.add(link)

    articles = []

    for link in links:
        category = None
        for _, cat in category_links:
            if _ == link:
                category = cat
                break

        article = parse_article(link)
        # article["category"] = category
        articles.append(article)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_in_seconds = int(elapsed_time)

    # Save the data to a JSON file
    data = {
        "source": "TechCrunch",
        "date": str(target_date),
        "no_of_articles": len(articles),
        "articles": articles
    }

    for article in data["articles"]:
        if isinstance(article.get("image_links"), set):
            article["image_links"] = list(article["image_links"]) 

    filename = f"techcrunch_articles_{target_date}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        logging.info(f"{len(articles)} articles scraped successfully and saved to {filename}!")
        logging.info(elapsed_time_in_seconds)
        return filename

    except (IOError, OSError) as file_error:
        logging.error(f"Error writing data to JSON file: {file_error}")
        return None

if __name__ == "__main__":
    date_input = input("Enter the date (YYYY-MM-DD): ")
    scrape_articles(date_input)