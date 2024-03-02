import json
import os

import requests
from dotenv import load_dotenv
from supabase import Client, create_client

# Load environment variables from a .env file
load_dotenv()

# Retrieve Supabase URL and API Key from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Create a Supabase client
supabase: Client = create_client(url, key)

target_date=str('2024-02-29')

file_url = f"https://tuwtkihewdnqtxitktpe.supabase.co/storage/v1/object/public/tech-crunch/{target_date}_TechCrunch.json"

response = requests.get(file_url)

data = response.json()

json_data = json.dumps(data, ensure_ascii=False, indent=4)


# Extract revised titles from the articles
revised_titles = [article.get('revised_title', '') for article in json_data.get('articles', [])]

# Print the extracted revised titles
for idx, title in enumerate(revised_titles, 1):
    print(f"Article {idx}: {title}")
