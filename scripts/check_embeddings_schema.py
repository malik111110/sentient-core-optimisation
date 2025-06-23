import psycopg2
from psycopg2 import sql
from pathlib import Path
from dotenv import load_dotenv
import os

def check_embeddings_schema():
    print("🔍 Checking document_embeddings table schema...")
    
    # Load environment variables
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    load_dotenv(env_path, override=True)
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return
    
    print(f"Connecting to: {db_url}")
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Get column information for document_embeddings
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'document_embeddings'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        if not columns:
            print("❌ document_embeddings table not found")
            return
            
        print("\n📋 document_embeddings table schema:")
        print(f"{'Column Name':<20} {'Data Type':<20} {'Nullable':<10} {'Default'}")
        print("-" * 60)
        
        for col in columns:
            col_name, data_type, is_nullable, col_default = col
            print(f"{col_name:<20} {data_type:<20} {is_nullable:<10} {col_default or ''}")
        
        # Check if vector index exists
        cursor.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'document_embeddings'
        """)
        
        indexes = cursor.fetchall()
        
        if indexes:
            print("\n🔍 Indexes on document_embeddings:")
            for idx in indexes:
                print(f"- {idx[0]}: {idx[1]}")
        else:
            print("\n⚠️ No indexes found on document_embeddings table")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error checking document_embeddings schema: {e}")

if __name__ == "__main__":
    check_embeddings_schema()
