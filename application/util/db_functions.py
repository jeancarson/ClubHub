from typing import Optional
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
    """
    Returns True if the given username exists in the database, and
    False otherwise.

    :param username: Username to check the existence of.
    """

    return query_db(f"SELECT username FROM users WHERE username={username!r}") is not None


def user_approved(username: str) -> bool:
    """
    Returns True if the given username corresponds to an approved
    user, and False otherwise.

    :param username: User to check approval of.
    """

    return query_db(f"SELECT username FROM users WHERE username={username!r} AND approved=1") is not None


def get_last_user() -> Row | None:
    """
    Fetches and returns the id of the last user in the database if present,
    and None otherwise.
    """

    return query_db("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1", single=True)


def create_user(
        *,
        username: str,
        password: str,
        user_type: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None) -> None:
    """
    Creates a new user in the database.
    ID is automatically generated. Users are not approved by default.
    """

    age: Optional[int] = int(age) if age is not None else None

    last_user: Row | None = get_last_user()
    user_id: int

    if last_user is None:
        user_id = 1
    else:
        user_id = last_user["user_id"] + 1

    modify_db(
        "INSERT INTO users"
        "(user_id, username, password, approved, first_name, last_name, age, email, phone, gender) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        user_id, username, password, 0, first_name, last_name, age, email, phone, gender
    )

    if user_type == "coordinator":
        modify_db("INSERT INTO coordinators (user_id) VALUES (?)", user_id)
    elif user_type == "student":
        modify_db("INSERT INTO students (user_id) VALUES (?)", user_id)


def get_users(table: Optional[str] = None) -> list[Row] | None:
    """
    Returns a list containing the rows from the given table, if there are any.

    :param table: Should be either "users" (default), "coordinators", or "students"
    """

    table: str = "users" if table is None else table
    results: list[Row] | None = query_db(f"SELECT user_id FROM {table}")

    if results is None:
        return None

    if table == "coordinators":
        # Include the admin coordinator too I suppose
        admin_results: list[Row] | None = query_db("SELECT user_id FROM administrators")

        if admin_results is not None:
            results.extend(admin_results)

    query_string: str = ", ".join(str(user["user_id"]) for user in results)

    return query_db(f"SELECT * FROM users WHERE user_id IN ({query_string})")


def delete_user(*, username: Optional[str] = None, user_id: Optional[int] = None) -> None:
    """
    Deletes a user, specified by either their username or user id, from the users table.

    Keyword Arguments:
        :param username: User's username. If this is given, their id cannot be.
        :param user_id: User's id. Likewise, if this is given, their username cannot be.

    Exactly of the above keyword arguments must be provided.
    """

    if (username is None and user_id is None) or (username is not None and user_id is not None):
        raise ValueError("Exactly one of the keyword arguments, username or user_id must be given")

    if username is not None:
        if not user_exists(username):
            return None

    elif user_id is not None:
        result = query_db(f"SELECT username FROM users WHERE user_id={user_id}", single=True)

        if result is None:
            return None

        username: str = result["username"]

    modify_db(f"DELETE FROM users WHERE username={username!r}")
