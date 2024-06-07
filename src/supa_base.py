import os
from dotenv import load_dotenv
from supabase import Client, create_client

# Load environment variables from a .env file
load_dotenv()

# Fetch Supabase URL and Key from environment variables
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload(bucket_name: str, path: str, file_path: str) -> None:
    """
    Upload a file to the specified Supabase storage bucket. If the file already exists,
    it will attempt to update the existing file.

    Parameters:
        bucket_name (str): The name of the storage bucket.
        path (str): The path where the file will be stored.
        file_path (str): The local path to the file to be uploaded.
    """
    try:
        supabase.storage.from_(bucket_name).upload(path=path, file=file_path)
        print("Successfully UPLOADED the content")
    except Exception as e:
        # Check if the error is due to a duplicate file
        if isinstance(e.args[0], dict) and e.args[0].get('error') == 'Duplicate':
            try:
                supabase.storage.from_(bucket_name).update(path=path, file=file_path)
                print("Successfully UPDATED the content")
            except Exception as update_e:
                print(f"Failed to update the content: {update_e}")
        else:
            print(f"An error occurred: {e}")

# Example usage:
# upload("tech-news", "data/2024-06-05_techcrunch.json", "data/2024-06-05_techcrunch.json")