from sqlite3 import Connection, Cursor, Row, connect
from typing import Optional

from flask import g

DB_PATH: str = "application/database/database.db"


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


def query_db(query: str, *args, single: Optional[bool] = None) -> list[Row] | Row | None:
    """
    Execute an SQLite query on the database.

    :param query: SQLite query to execute.

    Optional Arguments:
        :param args: Arguments to pass to the given query.

    Optional Keyword Arguments:
        :param single: If True, only returns the first value in the list of results (if there are any).

    :return: None if there are no results; otherwise, the list of results or the single result.

    Example:
        print(query_db("SELECT * FROM table))
    """

    single = False if single is None else single

    cursor: Cursor = get_db().cursor()
    cursor.execute(query, args)

    results: list[Row] = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    return results[0] if single else results


def modify_db(statement: str, *args) -> None:
    """
    Execute an SQLite manipulation statement on the database.

    :param statement: SQLite statement to perform.

    Optional Arguments:
        :param args: Arguments to pass to the given statement.

    Example:
        modify_db("INSERT INTO table VALUES (1, 17, 98)")
    """

    connection: Connection = get_db()
    cursor: Cursor = connection.cursor()

    cursor.execute(statement, args)
    connection.commit()

    cursor.close()


def last_id(table: str) -> Row | None:
    """
    Fetches and returns the ID of the last entry in the given table.
    Returns None if table is empty.

    :param table: Table name.
    """

    attr: str

    if table in ("users", "login"):
        attr = "user_id"
    elif table in ("events", "event_participants"):
        attr = "event_id"
    elif table in ("clubs", "club_memberships"):
        attr = "club_id"
    else:
        raise ValueError(f"Table {table!r} does not exist")

    return query_db(f"SELECT {attr} FROM {table} ORDER BY {attr} DESC LIMIT 1", single=True)
