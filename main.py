from src.generate import summarise
from src.scrape import scrape_articles
from src.supa_base import upload

import datetime

def main():
    date = datetime.date.today()
    filename = scrape_articles(str(date))
    summarise(filename)
    upload("tech-news",filename,filename)

if __name__ == "__main__":
    main()