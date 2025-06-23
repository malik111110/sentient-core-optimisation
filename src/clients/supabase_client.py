from supabase import create_client, Client
import os

def get_supabase_client() -> Client:
    """Initializes and returns a Supabase client instance."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set.")
        
    return create_client(url, key)
