#!/usr/bin/env python3
"""
Initialize Supabase local development environment.

This script helps set up the local Supabase environment by:
1. Creating necessary database schemas
2. Setting up initial tables
3. Configuring Row Level Security (RLS)
4. Creating initial roles and permissions
"""
import os
import sys
import time
import argparse
import logging
from typing import Optional, List
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('supabase-init')

class SupabaseInitializer:
    def __init__(self, db_url: str):
        """Initialize with database connection URL."""
        self.db_url = db_url
        self.conn = None

    def connect(self) -> bool:
        """Establish database connection with retry logic."""
        max_retries = 5
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                self.conn = psycopg2.connect(self.db_url)
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                logger.info("Successfully connected to the database")
                return True
            except psycopg2.OperationalError as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Connection attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {retry_delay} seconds..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error("Failed to connect to the database after multiple attempts")
                    raise
        return False

    def execute_sql_file(self, file_path: Path) -> bool:
        """Execute SQL commands from a file."""
        if not file_path.exists():
            logger.error(f"SQL file not found: {file_path}")
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql = f.read()
                
            with self.conn.cursor() as cur:
                cur.execute(sql)
                
            logger.info(f"Executed SQL file: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing {file_path.name}: {e}")
            self.conn.rollback()
            return False

    def setup_database(self, migrations_dir: Path) -> bool:
        """Set up the database by running all migration files."""
        if not migrations_dir.exists():
            logger.error(f"Migrations directory not found: {migrations_dir}")
            return False
            
        # Get all SQL files in the migrations directory
        migration_files = sorted([f for f in migrations_dir.glob('*.sql')])
        
        if not migration_files:
            logger.warning("No migration files found in the migrations directory")
            return False
            
        success = True
        for migration_file in migration_files:
            if not self.execute_sql_file(migration_file):
                logger.error(f"Failed to execute migration: {migration_file}")
                success = False
                break
                
        return success

    def close(self):
        """Close the database connection."""
        if self.conn is not None:
            self.conn.close()
            logger.info("Database connection closed")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Initialize Supabase local development environment')
    parser.add_argument(
        '--db-url',
        default=os.getenv('DATABASE_URL'),
        help='Database connection URL (default: from DATABASE_URL environment variable)'
    )
    parser.add_argument(
        '--migrations-dir',
        type=Path,
        default=Path('supabase/migrations'),
        help='Path to the migrations directory (default: supabase/migrations)'
    )
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    if not args.db_url:
        logger.error("Database URL is required. Either provide --db-url or set DATABASE_URL environment variable.")
        return 1
    
    initializer = SupabaseInitializer(args.db_url)
    
    try:
        if not initializer.connect():
            return 1
            
        logger.info("Starting database initialization...")
        
        if not initializer.setup_database(args.migrations_dir):
            logger.error("Database initialization failed")
            return 1
            
        logger.info("Database initialization completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1
    finally:
        initializer.close()

if __name__ == "__main__":
    sys.exit(main())
