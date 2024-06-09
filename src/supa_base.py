import json
import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_json(bucket_name: str, path: str, data: dict) -> None:
    """Uploads JSON data to a Supabase storage bucket."""
    try:
        supabase.storage.from_(bucket_name).upload(
            path=path, file=json.dumps(data).encode('utf-8') )

        print(f"Successfully uploaded JSON data to {path} in bucket {bucket_name}")
        
    except Exception as e:

        if isinstance(e.args[0], dict) and e.args[0].get('error') == 'Duplicate':
            try:
                supabase.storage.from_(bucket_name).update(path=path, file=json.dumps(data).encode('utf-8'))
                print("Successfully UPDATED the content")
            except Exception as update_e:
                print(f"Failed to update the content: {update_e}")
        else:
            print(f"An error occurred: {e}")

# Example usage:
# upload_json("your-bucket-name", "data/your_data.json", {"key": "value"})