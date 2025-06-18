import os
from supabase import create_client, Client

# Fetch Supabase URL and Service Key from environment variables
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY")

# Initialize the Supabase client
# We use the service key for backend operations, granting admin privileges.
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    # In a real application, you might raise an error or have a fallback,
    # but for now, we'll allow it to proceed and fail at runtime if not set,
    # or handle it gracefully in the persistence layer.
    print("WARNING: SUPABASE_URL or SUPABASE_SERVICE_KEY not set. Supabase client may not function.")
    supabase_client: Client | None = None
else:
    try:
        supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print(f"Supabase client initialized for URL: {SUPABASE_URL[:20]}...") # Log partial URL for confirmation
    except Exception as e:
        print(f"ERROR: Failed to initialize Supabase client: {e}")
        supabase_client: Client | None = None
