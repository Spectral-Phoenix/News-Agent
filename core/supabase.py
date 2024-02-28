import json
import os

import requests
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def upload(content, target_date):
    # Get the existing JSON file from Supabase Storage
    file_url = f"https://tuwtkihewdnqtxitktpe.supabase.co/storage/v1/object/public/tech-crunch/{target_date}_TechCrunch.json"
    
    try:
        response = requests.get(file_url)
        existing_data = response.json()

        # Check if 'no_of_articles' key is present in existing_data
        if 'no_of_articles' not in existing_data:
            # If not present, assume it's the first time
            existing_data = {
                "no_of_articles": len(content["articles"]),
                "articles": content["articles"]
            }
        else:
            # Update the article count
            existing_data["no_of_articles"] += len(content["articles"])
            # Append the new articles to the existing articles list
            existing_data["articles"].extend(content["articles"])

    except json.decoder.JSONDecodeError:
        # If the file doesn't exist or cannot be decoded as JSON, assume it's the first time
        existing_data = {
            "no_of_articles": len(content["articles"]),
            "articles": content["articles"]
        }

    # Convert the updated data to JSON
    json_data = json.dumps(existing_data, ensure_ascii=False, indent=4)
    json_buffer = json_data.encode('utf-8')

    try:
        # Upload the updated JSON file to Supabase Storage
        supabase.storage.from_("tech-crunch").update(file=json_buffer, path=f"{target_date}_TechCrunch.json")
        msg = f"Content updated to Supabase Storage: {target_date}_TechCrunch.json"
        print(msg)

    except Exception:
        # If the file doesn't exist yet, upload it
        supabase.storage.from_("tech-crunch").upload(file=json_buffer, path=f"{target_date}_TechCrunch.json")
        msg = f"Content saved to Supabase Storage: {target_date}_TechCrunch.json"
        print(msg)
