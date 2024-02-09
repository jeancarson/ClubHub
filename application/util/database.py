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
    return query_db(f"SELECT * FROM login WHERE username={username!r}") is not None


def create_new_user(**attributes) -> None:

    _age: str = attributes["age"]
    age: int | None = int(_age) if _age is not None else None

    last_user: None | Row = query_db("SELECT * FROM login ORDER BY userID DESC LIMIT 1", single=True)
    user_id: int

    if last_user is None:
        user_id = 1
    else:
        user_id = last_user["userID"] + 1

    modify_db(
        "INSERT INTO login (userID, username, password) VALUES (?, ?, ?)",
        user_id, attributes["username"], attributes["password"])

    # TODO: This
    # modify_db(
    #     "INSERT INTO users (user, first_name, last_name, age, email, phone, gender) VALUES (?, ?, ?, ?, ?, ?, ?)",
    #     user_id, attributes["first_name"], attributes["last_name"], attributes["age"],
    #     attributes["email"], attributes["phone"], attributes["gender"]
    # )
