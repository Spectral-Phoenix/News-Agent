import datetime

from src.generate import summarise
from src.rank import rank
from src.scrape import scrape_articles
from src.supa_base import upload

def main():
    
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    
    filename = scrape_articles(date_str)
    ranked_filename = f"{date_str}_technews.json"
    summarise(filename)
    rank(yesterday)
    upload("tech-news", filename, filename)
    upload("tech-news", ranked_filename, ranked_filename)

if __name__ == "__main__":
    main()
