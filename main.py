import datetime
from src.scrape import scrape_articles
from src.generate import generate_summaries_and_titles
from src.rank import rank_articles
from src.supa_base import upload_json
from app import start_discord_bot

def main():
    """Main function to orchestrate the entire process."""
    
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    scraped_data = scrape_articles(yesterday)
    if scraped_data:
        articles_with_summaries = generate_summaries_and_titles(scraped_data.copy())
        ranked_articles = rank_articles(articles_with_summaries.copy())
        
        if ranked_articles:
            upload_json("tech-news", f"data/{yesterday}_techcrunch.json", scraped_data)
            upload_json("tech-news", f"{yesterday}_technews.json", ranked_articles)
            start_discord_bot(ranked_articles['articles'])

if __name__ == "__main__":
    main()
