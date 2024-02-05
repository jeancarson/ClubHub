from sqlite3 import Connection, Cursor, Row, connect
from flask import g


DB_PATH: str = "application/database.db"


def get_db() -> Connection:
    """
    Returns the global database connection instance.
    """

    db: Connection | None = getattr(g, "_database", None)

    if db is None:
        db: Connection = connect(DB_PATH)
        db.row_factory = Row
        g._database = db

    return db


def query_db(query: str, *args, single: bool = False) -> list[Row] | Row | None:
    cur: Cursor = get_db().execute(query, *args)
    results: list[Row] = cur.fetchall()
    cur.close()

    if not results:
        return None

    return results[0] if single else results
