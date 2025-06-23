import os
import sys
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

def check_database():
    # Get the absolute path to the project root
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    
    print(f"Loading .env from: {env_path}")
    
    # Load environment variables from .env file explicitly
    if not load_dotenv(env_path, override=True):
        print(f"Warning: Could not load .env file from {env_path}")
    
    # Get database URL from environment
    db_url = os.getenv('DATABASE_URL')
    print(f"Database URL from .env: {db_url}")
    
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        print("Current environment variables:")
        for k, v in os.environ.items():
            if 'PASS' not in k and 'SECRET' not in k and 'KEY' not in k:
                print(f"{k}={v}")
        return
    
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return
    
    try:
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # List all tables in the public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print("\nFound the following tables in the database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in the database.")
            
        # Check if pgvector extension is installed
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'pgvector'")
        if cursor.fetchone():
            print("\n✅ pgvector extension is installed")
        else:
            print("\n❌ pgvector extension is NOT installed")
        
        # Close the connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error connecting to the database: {e}")
        print(f"Database URL: {db_url}")

if __name__ == "__main__":
    print("🔍 Checking database connection and schema...")
    check_database()
