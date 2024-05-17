from bs4 import BeautifulSoup
from typing import List
import requests

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

def main():

    

    
    count = 0
    for url in urls:
        blacklist = ['sportstar.thehindu.com', 'thehindubusinessline.com']
        links = scrape_links(url,blacklist)
        count += len(links)
        

    print(f"Total Links: {count}")
    print(f"Unique Links: {len(linked_list)}")

    

if __name__ == '__main__':
    main()

