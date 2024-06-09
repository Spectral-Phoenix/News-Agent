import datetime
from src.scrape import scrape_articles
from src.generate import generate_summaries_and_titles
from src.rank import rank_articles
from src.supa_base import upload_json
from app import start_discord_bot
import logging

logging.basicConfig(level=logging.INFO)

def main():
    """Main function to orchestrate the entire process."""
    
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        scraped_data = scrape_articles(yesterday)
        if not scraped_data:
            logging.warning("No articles scraped. Skipping further processing.")
            return  # Stop execution if no articles were scraped

        try:
            articles_with_summaries = generate_summaries_and_titles(scraped_data.copy())
        except Exception as e:
            logging.error(f"Error generating summaries and titles: {e}")
            articles_with_summaries = None  # Ensure the variable is defined even after an error

        if articles_with_summaries:
            try:
                ranked_articles = rank_articles(articles_with_summaries.copy())
            except Exception as e:
                logging.error(f"Error ranking articles: {e}")
                ranked_articles = None 

            if ranked_articles:
                try:
                    upload_json("tech-news", f"data/{yesterday}_techcrunch.json", scraped_data)
                except Exception as e:
                    logging.error(f"Error uploading scraped data to Supabase: {e}")
                try:
                    upload_json("tech-news", f"{yesterday}_technews.json", ranked_articles)
                except Exception as e:
                    logging.error(f"Error uploading ranked articles to Supabase: {e}")
                try:
                    start_discord_bot(ranked_articles['articles'])
                    logging.info("Job Completed Successfully!")
                except Exception as e:
                    logging.error(f"Error starting Discord bot: {e}")
            else:
                logging.warning("No ranked articles to process.")
        else:
            logging.warning("No articles with summaries to process.")

    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()