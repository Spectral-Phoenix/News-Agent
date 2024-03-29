import json
import logging
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_json_file(target_date):
    """
    Load JSON data from a specified URL based on the target date.

    Parameters:
        target_date (str): The target date in the format 'YYYY-MM-DD'.

    Returns:
        dict: Parsed JSON data.
    """
    try:
        json_url = f"https://tuwtkihewdnqtxitktpe.supabase.co/storage/v1/object/public/tech-crunch/{target_date}_TechCrunch.json"
        response = requests.get(json_url)
        response.raise_for_status()  # Raise an exception if the request failed (non-2xx status code)
        json_data = response.json()  # Directly parse the JSON content from the response
        return json_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error loading JSON file: {e}")
        return {}

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
    Parse article content from a specified article URL.

    Parameters:
        link (str): URL of the article.

    Returns:
        dict or None: Parsed article data or None if parsing fails.
    """
    try:
        article = requests.get(link)
        article.raise_for_status()
        soup = BeautifulSoup(article.text, 'lxml')

        title_element = soup.find('h1')
        content_element = soup.find('div', class_='article-content')

        if title_element is not None and content_element is not None:
            image_links = [img['src'] for img in soup.find_all('img')]
            return {
                "title": title_element.get_text(),
                "content": content_element.get_text(),
                "image_links": image_links,
                "link": link,
            }
        else:
            logging.error(f"Error parsing article content for {link}: Title or content not found.")
            return None

    except requests.exceptions.RequestException as req_exc:
        logging.error(f"Error fetching article content for {link}: {req_exc}")
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

    # Load the JSON file
    json_file = load_json_file(target_date=date_input)
    existing_articles = {a["link"]: a for a in json_file.get("articles", [])}

    for link in links:
        category = None
        for _, cat in category_links:
            if _ == link:
                category = cat
                break

        article = parse_article(link)
        if article and article["link"] not in existing_articles:  
            article["category"] = category
            articles.append(article)
            existing_articles[article["link"]] = article  # Add parsed article to the dictionary

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

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    json_buffer = json_data.encode('utf-8')

    time_taken_msg = "Time taken to scrape: " + str(elapsed_time_in_seconds) + " seconds"
    logging.info(f"{len(articles)} articles scraped successfully!")
    logging.info(time_taken_msg)

    return json_buffer
