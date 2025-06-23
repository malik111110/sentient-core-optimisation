import os
import sys
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

def main():
    print("🔍 Checking database tables...")
    
    # Load environment variables
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    load_dotenv(env_path, override=True)
    
    # Get database connection details
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return
        
    print(f"Connecting to: {db_url}")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if vector extension exists
        cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        if cursor.fetchone():
            print("✅ pgvector extension is installed")
        else:
            print("❌ pgvector extension is not installed")
            
        # List all tables in the public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print("\n📋 Found tables:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("\nℹ️ No tables found in the public schema")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error connecting to the database: {e}")
        print(f"Database URL: {db_url}")

if __name__ == "__main__":
    main()
