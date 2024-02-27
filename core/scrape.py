import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import time

def load_json_file(target_date):
    try:
        json_url = f"https://tuwtkihewdnqtxitktpe.supabase.co/storage/v1/object/public/tech-crunch/{target_date}_TechCrunch.json"
        print(json_url)
        response = requests.get(json_url)
        response.raise_for_status()  # Raise an exception if the request failed (non-2xx status code)
        json_data = response.json()  # Directly parse the JSON content from the response
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error loading JSON file: {e}")
        return {}

def extract_date(link):
    match = re.search(r"/(\d{4}/\d{2}/\d{2})/", link)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%Y/%m/%d").date()
    else:
        return None

def scrape_links(category_url, category):
    try:
        resp = requests.get(category_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        return [(a['href'], category) for a in soup.select('h2 a')]
    except requests.exceptions.RequestException as req_exc:
        print(f"Error scraping {category_url}: {req_exc}")
        return []

def parse_article(link):
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
            print(f"Error parsing article content for {link}: Title or content not found.")
            return None

    except requests.exceptions.RequestException as req_exc:
        print(f"Error fetching article content for {link}: {req_exc}")
        return None

    except Exception as e:
        print(f"Error parsing article content for {link}: {e}")
        return None

def scrape_articles(date_input):
    if not date_input:
        print("Please provide a valid date.")
        return
    try:
        target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Config
    BASE_URL = "https://techcrunch.com/category/"
    CATEGORIES = ["artificial-intelligence", "apps", "biotech-health", "climate", "commerce",
                  "enterprise", "fintech", "gadgets", "gaming", "government-policy", "hardware",
                  "media-entertainment", "privacy", "robotics", "security", "social", "space",
                  "startups", "transportation", "venture"]

    print("Fetching articles...")

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
    print(f"{len(articles)} articles scraped successfully!")
    print(time_taken_msg)

    return json_buffer
