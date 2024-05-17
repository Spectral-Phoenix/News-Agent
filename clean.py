import json
import requests
import logging
import os
from dotenv import load_dotenv
from supabase import Client, create_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

# Retrieve Supabase URL and API Key from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Create a Supabase client
supabase: Client = create_client(url, key)

def clean_data(data):
    def remove_non_ascii(text):
        return ''.join(i for i in text if ord(i) < 128)
    
    if isinstance(data, dict):
        return {clean_data(k): clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(v) for v in data]
    elif isinstance(data, str):
        return remove_non_ascii(data)
    else:
        return data

def clean_and_upload_to_supabase(target_date):
    """
    Loads JSON content from Supabase Storage, cleans it, and uploads it back to Supabase.

    Parameters:
        target_date (str): Date used in the filename for storage.

    Raises:
        Exception: Any exception encountered during the Supabase storage operation.

    Returns:
        None
    """
    # Get the existing JSON file from Supabase Storage
    file_path = f"https://tuwtkihewdnqtxitktpe.supabase.co/storage/v1/object/public/tech-crunch/{target_date}_TechCrunch.json"

    try:
        # Try to retrieve existing data from the file
        response = requests.get(file_path)
        existing_data = response.json()

        # Clean non-ASCII characters
        cleaned_data = clean_data(existing_data)

    except Exception:
        # Handle exceptions appropriately
        logger.error("Error while loading data from Supabase Storage.")
        return

    # Convert the cleaned data to JSON
    json_data = json.dumps(cleaned_data, ensure_ascii=False, indent=4)
    json_buffer = json_data.encode("utf-8")

    try:
        # Upload the cleaned JSON file to Supabase Storage
        supabase.storage.from_("tech-crunch").update(
            file=json_buffer, path=f"{target_date}_TechCrunch.json"
        )
        #supabase.storage.from_("tech-crunch").update(file=json_buffer, path=file_path)
        msg = f"Cleaned content updated to Supabase Storage: {target_date}_TechCrunch.json"
        logger.info(msg)

    except Exception:
        logger.error("Error while uploading cleaned data to Supabase Storage.")

# Example usage
for i in range(1,25):
    target_date = str(f"2024-03-{i}")
    clean_and_upload_to_supabase(target_date)
