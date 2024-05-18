import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def upload(bucket_name, path, file_path):

    try:
        supabase.storage.from_(bucket_name).upload(path=path, file=file_path)
        print("Successfully UPLOADED the content")
    except Exception as e:
        if e.args[0].get('error') == 'Duplicate':
            try:
                supabase.storage.from_(bucket_name).update(path=path, file=file_path)
                print("Successfully UPDATED the content")
            except Exception as update_e:
                print(f"Failed to update the content: {update_e}")
        else:
            print(f"An error occurred: {e}")
