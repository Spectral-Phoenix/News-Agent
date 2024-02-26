import os
import json

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def upload(content, target_date):
    json_data = json.dumps(content, ensure_ascii=False, indent=4)
    json_buffer = json_data.encode('utf-8')

    try:
        supabase.storage.from_("tech-crunch").upload(file=json_buffer, path=f"{target_date}_TechCrunch.json")
        msg = f"Content saved to Supabase Storage: {target_date}_TechCrunch.json"
        print(msg)

    except Exception :
        supabase.storage.from_("tech-crunch").update(file=json_buffer, path=f"{target_date}_TechCrunch.json")
        msg_update = f"Content updated to Supabase Storage: {target_date}_TechCrunch.json"
        print(msg_update)
