import json
import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, datetime
from typing import Dict, List, Set

import requests
from bs4 import BeautifulSoup
from newspaper import Article

from core.supa_base import upload

logging.basicConfig(level=logging.ERROR)

BLACKLIST_FILE_PATH = 'data/the_hindu/blacklist.json'

def is_blacklisted(url: str, blacklist: List[str]) -> bool:
    domain = url.split('//')[1].split('/')[0]
    return domain in blacklist

def scrape_links(url: str, blacklist: List[str] = None) -> Set[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = {link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.ece')}
    if blacklist:
        links = {link for link in links if not is_blacklisted(link, blacklist)}
    return links

def scrape_text(link: str) -> Dict[str, str]:
    try:
        article = Article(link, language='en')
        article.download()
        article.parse()
        article_date = article.publish_date.date() if article.publish_date else None
        if article_date == date.today():
            return {
                'title': article.title,
                'publish_date': article.publish_date.strftime('%Y-%m-%d') if article.publish_date else 'N/A',
                'text': article.text,
                'url': link,
            }
    except Exception:
        logging.error(f"Unexpected error occurred while scraping {link}")
    return None

def scrape_links_from_urls(urls: List[str], blacklist: List[str]) -> Set[str]:
    all_links = set()
    for url in urls:
        all_links.update(scrape_links(url, blacklist))
    return all_links

def load_previous_urls(file_path: str) -> Set[str]:
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        data = json.load(f)
        return {article['url'] for article in data.get('articles', [])}

def load_blacklist(file_path: str) -> Set[str]:
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        return set(json.load(f))

def save_blacklist(file_path: str, blacklist: Set[str]):
    with open(file_path, 'w') as f:
        json.dump(list(blacklist), f, ensure_ascii=True, indent=4)

def main():
    start_time = datetime.now()

    urls = [
        'https://www.thehindu.com/news/national/', 'https://www.thehindu.com/news/international/', 'https://www.thehindu.com/news/national/andhra-pradesh/',
        'https://www.thehindu.com/news/national/karnataka/', 'https://www.thehindu.com/news/national/kerala/', 'https://www.thehindu.com/news/national/tamil-nadu/',
        'https://www.thehindu.com/news/national/telangana/', 'https://www.thehindu.com/news/cities/Vijayawada/', 'https://www.thehindu.com/business/',
        'https://www.thehindu.com/business/agri-business/', 'https://www.thehindu.com/business/Economy/', 'https://www.thehindu.com/business/Industry/',
        'https://www.thehindu.com/business/markets/', 'https://www.thehindu.com/business/budget/', 'https://www.thehindu.com/sci-tech/',
        'https://www.thehindu.com/sci-tech/science/', 'https://www.thehindu.com/sci-tech/technology/', 'https://www.thehindu.com/sci-tech/health/',
        'https://www.thehindu.com/sci-tech/agriculture/', 'https://www.thehindu.com/sci-tech/energy-and-environment/', 'https://www.thehindu.com/sci-tech/technology/gadgets/',
        'https://www.thehindu.com/sci-tech/technology/internet/'
    ]

    blacklist_domains = ['sportstar.thehindu.com', 'thehindubusinessline.com']

    # Load URL blacklist
    url_blacklist = load_blacklist(BLACKLIST_FILE_PATH)

    # Collect all links first
    url_list = scrape_links_from_urls(urls, blacklist_domains)

    # Load previously scraped URLs
    previous_file_path = f"data/the_hindu/{str(date.today())}_the_hindu.json"
    previous_urls = load_previous_urls(previous_file_path)

    # Filter out previously scraped and blacklisted URLs
    new_urls = url_list - previous_urls - url_blacklist

    data = {"source": "the-hindu", "articles": []}

    # Use ProcessPoolExecutor to scrape articles concurrently
    with ProcessPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scrape_text, link): link for link in new_urls}
        for i, future in enumerate(as_completed(future_to_url), start=1):
            link = future_to_url[future]
            try:
                text_data = future.result()
                if text_data:
                    data["articles"].append(text_data)
                else:
                    url_blacklist.add(link)  # Add to blacklist if not from today's date
                print(f"Scraped {i} out of {len(new_urls)}")
            except Exception as exc:
                logging.error(f"Error scraping {link}: {exc}")

    data["no_of_articles"] = len(data["articles"])

    today = str(date.today())
    file_path = f"{today}_the_hindu.json"

    with open(f'data/the_hindu/{file_path}', 'w') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

    print("Scraping Completed")
    # Upload the JSON File to Supabase
    upload("tech-crunch", file_path, f"data/the_hindu/{file_path}")

    # Save the updated URL blacklist
    save_blacklist(BLACKLIST_FILE_PATH, url_blacklist)

    end_time = datetime.now()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time}")

if __name__ == "__main__":
    main()