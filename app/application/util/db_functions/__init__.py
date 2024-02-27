from sqlite3 import Connection, Cursor, Row, connect
from typing import Optional
from pathlib import Path

from flask import g


ROOT_DIR: Path = Path(__file__).parents[4]
DB_DIR: Path = ROOT_DIR / "app" / "application" / "database"

DB_PATH: Path = DB_DIR / "database.db"
SCHEMA_PATH: Path = DB_DIR / "schema.sql"
POPULATE_PATH: Path = DB_DIR / "populate.sql"

DDL_BACKUP_PATH: Path = ROOT_DIR / "ddl_backup.sql"


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


def dump_ddl() -> str:
    """
    Returns a string containing all DDL statements,
    exported from the database.

    This function is called once (automatically) in initialise_db().
    """

    output: list[str] = []
    results: list[Row] = query_db("SELECT sql FROM sqlite_master")

    for row in results:
        sql: str | None = row["sql"]

        if sql is not None:
            output.append(sql)

    return "\n\n".join(output)
