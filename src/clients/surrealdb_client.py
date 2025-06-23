# SurrealDB Client Initialization

import os
from surrealdb import Surreal

async def get_surrealdb_client():
    """Initializes and returns a SurrealDB client instance."""
    db_url = os.getenv("SURREALDB_URL", "ws://localhost:8000/rpc")
    db_user = os.getenv("SURREALDB_USER", "root")
    db_pass = os.getenv("SURREALDB_PASS", "root")
    db_ns = os.getenv("SURREALDB_NS", "sentient_core")
    db_name = os.getenv("SURREALDB_DB", "sentient_db")

    try:
        db = Surreal(db_url)
        await db.connect()
        await db.signin({"user": db_user, "pass": db_pass})
        await db.use(db_ns, db_name)
        print(f"Successfully connected to SurrealDB at {db_url}")
        return db
    except Exception as e:
        print(f"Failed to connect to SurrealDB: {e}")
        return None

# Example of how to use the client in other modules:
# from .surrealdb_client import get_surrealdb_client
# async def some_function():
#     db = await get_surrealdb_client()
#     if db:
#         # Use db for operations
#         await db.close()
