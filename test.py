import json
import logging
from datetime import date
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from newspaper  import Article

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
        # images = article.top_image
        
        if article_date == date.today():
            return {
                'title': article.title,
                'publish_date': article.publish_date.strftime('%Y-%m-%d'),
                'text': article.text,
                'url': link,
                # 'images': images
            }
    except Exception:
        logging.error(f"Unexpected error occurred while scraping {link}")
    return None

def main():

    urls = ["https://techcrunch.com/category/artificial-intelligence", 
                    "https://techcrunch.com/category/apps", "https://techcrunch.com/category/biotech-health", "https://techcrunch.com/category/climate", "https://techcrunch.com/category/commerce",
                  "https://techcrunch.com/category/enterprise", "https://techcrunch.com/category/fintech", "https://techcrunch.com/category/gadgets", "https://techcrunch.com/category/gaming", "https://techcrunch.com/category/government-policy", "https://techcrunch.com/category/hardware",
                  "https://techcrunch.com/category/media-entertainment", "https://techcrunch.com/category/privacy", "https://techcrunch.com/category/robotics", "https://techcrunch.com/category/security", "https://techcrunch.com/category/social", "https://techcrunch.com/category/space",
                  "https://techcrunch.com/category/startups", "https://techcrunch.com/category/transportation", "https://techcrunch.com/category/venture"]
                  
    url_list = set()

    for url in urls:
        links = scrape_links(url)
        print(f"No of Links: {len(links)}")
        url_list.update(links)
    
    # with open('links.txt', 'w') as f:
    #     for link in url_list:
    #         f.write(f"{link}\n")
    #     print("Links Saved to links.txt")

    scraped_data = []
    for i, link in enumerate(url_list, start=1):
        print(f"Scraping {i} out of {len(url_list)}")
        text_data = scrape_text(link)
        if text_data:
            scraped_data.append(text_data)

    today = str(date.today())
    file_path =  f"{today}_the_hindu.json"

    with open(f'core/hindu/{file_path}', 'w') as f:
        f.write(scraped_data)
        print("Scraping Completed")

if __name__ == "__main__":
    main()