import schedule
import time

from core.generate import summarise
from core.scrape import scrape_articles
from core.supabase import upload

from datetime import date

def process(date_input):
    content = scrape_articles(date_input)
    summarised_content = summarise(content)
    return summarised_content

def job():
    date_input = str(date.today())
    print(f"Job started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    content = process(date_input)
    upload(content, date_input)
    print(f"Job completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Scheduling next job in 1 hour...")

# Run the first job immediately
job()

# Schedule subsequent jobs to run every hour
schedule.every().hour.do(job)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
