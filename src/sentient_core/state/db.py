"""Connection pool / singleton for SurrealDB.

The rest of the state layer imports `get_db()` to obtain a shared async
connection.  We connect lazily and reuse the same `Surreal` instance for every
call to avoid WebSocket reconnections.
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

from surrealdb import Surreal

_DB_LOCK = asyncio.Lock()
_db_instance: Optional[Surreal] = None


async def get_db() -> Surreal:
    """Return a global SurrealDB connection, establishing it if necessary."""
    global _db_instance

    if _db_instance is not None:
        return _db_instance

    async with _DB_LOCK:
        if _db_instance is None:
            url = os.getenv("SURREALDB_URL", "ws://localhost:8000/rpc")
            user = os.getenv("SURREALDB_USERNAME", "root")
            pw = os.getenv("SURREALDB_PASSWORD", "root")
            ns = os.getenv("SURREALDB_NAMESPACE", "sentient_core")
            db_name = os.getenv("SURREALDB_DATABASE", "agents")

            db = Surreal(url)
            await db.connect()
            await db.signin({"user": user, "pass": pw})
            await db.use(ns, db_name)

            _db_instance = db
        return _db_instance
