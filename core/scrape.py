import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import time

def scrape_articles():
    date_input = "2024-02-24"

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
        except Exception as e:
            print(f"Error scraping {category_url}: {e}")
            return []
    
    def parse_article(link):
        article = requests.get(link)
        soup = BeautifulSoup(article.text, 'lxml')
        image_links = [img['src'] for img in soup.find_all('img')]
        return {
            "title": soup.find('h1').get_text(),
            "content": soup.find('div', class_='article-content').get_text(),
            "image_links": image_links,
            "link": link,
        }

    print("Fetching articles...")
    
    start_time = time.time()
    links = {}  # Dictionary to store unique links
    
    for category in CATEGORIES:
        category_url = BASE_URL + category + "/"
        category_links = scrape_links(category_url, category)
        for link, category in category_links:
            date = extract_date(link)
            if date == target_date and link not in links:
                # Check if the link is already in the 'links' dictionary
                links[link] = category
    
    articles = []

    for link, category in links.items():
        article = parse_article(link)
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
