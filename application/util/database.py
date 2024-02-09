from sqlite3 import Connection, Cursor, Row, connect

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


def query_db(query: str, *args, single: bool = False) -> list[Row] | Row | None:
    """
    Execute an SQLite query on the database.

    :param query: SQLite query to execute.
    :param args: Arguments to pass to the given query.
    :param single: If True, only returns the first value in the list of results (if there are any).
    :return: None if there are no results; otherwise, the list of results or the single result.

    Example:
        print(query_db("SELECT * FROM table))
    """

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
    :param args: Arguments to pass to the given statement.

    Example:
        modify_db("INSERT INTO table VALUES (1, 17, 98)")
    """

    connection: Connection = get_db()
    cursor: Cursor = connection.cursor()

    cursor.execute(statement, args)
    connection.commit()

    cursor.close()


def user_exists(username: str) -> bool:
    return query_db(f"SELECT * FROM users WHERE username={username!r}") is not None


def user_approved(username: str) -> bool:
    return query_db(f"SELECT * FROM users WHERE username={username!r} AND approved=1") is not None


def create_new_user(**attributes) -> None:

    user_type: str = attributes["user_type"]

    _age: str = attributes["age"]
    age: int | None = int(_age) if _age is not None else None

    last_user: None | Row = query_db("SELECT * FROM users ORDER BY user_id DESC LIMIT 1", single=True)
    user_id: int

    if last_user is None:
        user_id = 1
    else:
        user_id = last_user["user_id"] + 1

    modify_db(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        user_id, attributes["username"], attributes["password"], 0, attributes["first_name"],
        attributes["last_name"], attributes["age"], attributes["email"], attributes["phone"],
        attributes["gender"]
    )

    if user_type == "coordinator":
        modify_db("INSERT INTO coordinators (user_id) VALUES (?)", user_id)
    elif user_type == "student":
        modify_db("INSERT INTO students (user_id) VALUES (?)", user_id)
