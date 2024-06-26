import json
import logging
from datetime import date
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from newspaper import Article

from supa_base import upload

logging.basicConfig(level=logging.ERROR)

def is_blacklisted(url: str, blacklist: List[str]) -> bool:
    domain = url.split('//')[-1].split('/')[0]
    return domain in blacklist

def scrape_links(url: str, blacklist: List[str] = None) -> set[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = {link['href'] for link in soup.find_all('a') if link.get('href') and link['href'].endswith('.ece')}
    if blacklist:
        links = {link for link in links if not is_blacklisted(link, blacklist)}
    return links

def scrape_text(link: str) -> Dict[str, str]:
    try:
        article = Article(link, language='en')
        article.download()
        article.parse()
        article_date = article.publish_date.date()
        images = article.images
        try:
            image_link = [image for image in images if image.startswith('https://th-i.thgim.com/')][0]
        except Exception:
            image_link = None
        if article_date == date.today():

            if len(article.text) >= 130:
                return {
                    'title': article.title,
                    'publish_date': article.publish_date.strftime('%Y-%m-%d'),
                    'text': article.text,
                    'url': link,
                    'image' : image_link,
                }
    except Exception as e:
        logging.error(f"Unexpected error occurred while scraping {link}")
        print(e)
    return None

def main():
    urls = ['https://www.thehindu.com/news/national/', 'https://www.thehindu.com/news/international/', 'https://www.thehindu.com/business/',
            'https://www.thehindu.com/business/agri-business/', 'https://www.thehindu.com/business/Economy/', 'https://www.thehindu.com/business/Industry/',
            'https://www.thehindu.com/business/budget/', 'https://www.thehindu.com/sci-tech/',
            'https://www.thehindu.com/sci-tech/science/', 'https://www.thehindu.com/sci-tech/technology/', 'https://www.thehindu.com/sci-tech/health/',
            'https://www.thehindu.com/sci-tech/agriculture/', 'https://www.thehindu.com/sci-tech/energy-and-environment/', 'https://www.thehindu.com/sci-tech/technology/gadgets/',
            'https://www.thehindu.com/sci-tech/technology/internet/']
    blacklist = ['sportstar.thehindu.com', 'thehindubusinessline.com']
    url_list = set()
    for url in urls:
        links = scrape_links(url, blacklist)
        print(f"No of Links: {len(links)}")
        url_list.update(links)

    today = str(date.today())
    file_path = f"{today}_the_hindu.json"
    
    # Check if the file already exists
    try:
        with open(f'data/the_hindu/{file_path}', 'r') as f:
            existing_data = json.load(f)
            existing_urls = {article['url'] for article in existing_data['articles']}
    except FileNotFoundError:
        existing_data = None
        existing_urls = set()
    
    data = {
        "source": "the-hindu",
        "articles": []
    }

    for i, link in enumerate(url_list, start=1):
        print(f"Scraping {i} out of {len(url_list)}")
        if link not in existing_urls:
            text_data = scrape_text(link)
            if text_data:
                data["articles"].append(text_data)
        else:
            print(f"Skipping {link} as it already exists in the JSON file.")

    data["no_of_articles"] = len(data["articles"])
    
    # Merge existing data with new data
    if existing_data:
        existing_data["articles"].extend(data["articles"])
        existing_data["no_of_articles"] = len(existing_data["articles"])
        data = existing_data

    with open(f'data/the_hindu/{file_path}', 'w') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

    print("Scraping Completed")
    upload("tech-crunch", file_path, f"data/the_hindu/{file_path}")

if __name__ == "__main__":
    main()