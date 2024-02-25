import json
import re
import time
import io
from datetime import date, datetime
import os

from supabase import create_client, Client
import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def scrape_articles():
    target_date = date.today()

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

    def get_links_for_date(target_date):
        links = {}  # Dictionary to store unique links
        for category in CATEGORIES:
            category_url = BASE_URL + category + "/"
            category_links = scrape_links(category_url, category)
            for link, category in category_links:
                date = extract_date(link)
                if date == target_date and link not in links:
                    # Check if the link is already in the 'links' dictionary
                    links[link] = category
        return links

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
    links = get_links_for_date(target_date)
    articles = []
    for link, category in links.items():
        article = parse_article(link)
        article["category"] = category
        articles.append(article)
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_taken = int(elapsed_time)

    # Save the data to Supabase Storage
    data = {
        "source": "TechCrunch",
        "date": str(target_date),
        "no_of_articles": len(articles),
        "articles": articles
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    json_buffer = json_data.encode('utf-8')

    try:
        with supabase.storage.from_("tech-crunch").upload(file= json_buffer, path=f"{target_date}_TechCrunch.json") as response:
            if response.status_code == 200:
                print(f"{len(articles)} articles uploaded successfully!")
                msg = f"Content saved to Supabase Storage: {target_date}_TechCrunch.json"
                print(msg)
            else:
                print(f"Error uploading to Supabase Storage: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception while uploading to Supabase Storage: {e}")

    time_taken_str = "Time taken to scrape: " + str(time_taken) + " seconds"
    print(time_taken_str)


scrape_articles()