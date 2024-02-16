from sqlite3 import Connection, Cursor, Row, connect
from typing import Optional

from flask import g, current_app

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

    return query_db(f"SELECT username FROM login WHERE username={username!r}", single=True) is not None


def last_user_id() -> Row | None:
    """
    Fetches and returns the id of the last user in the database if present,
    and None otherwise.
    """

    return query_db("SELECT user_id FROM login ORDER BY user_id DESC LIMIT 1", single=True)


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
        gender: Optional[str] = None) -> bool:
    """
    Creates a new user in the database.
    ID is automatically generated. Users are not approved by default.

    :return: True if user is the first on the system, False otherwise.
    """

    age: int | None = int(age) if age is not None else None

    last_user: Row | None = last_user_id()
    user_id: int
    approved: str

    if last_user is None:
        user_id = 1
        user_type = "ADMINISTRATOR"
        approved = "APPROVED"  # Override approval if registration is the first on the system
    else:
        user_id = last_user["user_id"] + 1
        user_type = user_type.upper()
        approved = "PENDING"

    modify_db(
        """
        INSERT INTO users 
        (user_id, first_name, last_name, age, email, phone, gender, password, user_type, approved) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        user_id, first_name, last_name, age, email, phone, gender, password, user_type, approved
    )

    modify_db(
        """
        INSERT INTO login
        (user_id, username) VALUES
        (?, ?)
        """,
        user_id, username
    )

    if user_type == "ADMINISTRATOR":
        return True

    return False


def get_users_info(
        *,
        user_type: Optional[str] = None,
        unapproved: Optional[bool] = None,
        admin_permission: Optional[bool] = None) -> list[Row] | None:
    """
    Returns a list containing the rows from the users table, if there are any.

    :param user_type: Should be either "STUDENT", "COORDINATOR", "ADMIN", or None (for all users).
    :param unapproved: Only includes unapproved users.
    :param admin_permission: If true, also includes username in results.
    """

    user_results: list[Row] | None
    login_results: list[Row] | None
    condition: str

    current_app.logger.info(user_type)

    if user_type is None:
        if unapproved:
            condition = "WHERE users.approved='UNAPPROVED'"
        else:
            condition = ";"

        if admin_permission:
            user_results = query_db(f"""
                SELECT *
                FROM users
                FULL OUTER JOIN login
                ON users.user_id = login.user_id
                {condition}
            """)
        else:
            user_results = query_db("SELECT * FROM users")
    else:
        join_type: str

        if unapproved:
            condition = " AND users.approved='UNAPPROVED';"
        else:
            condition = ";"

        if admin_permission:
            join_type = "FULL OUTER"
        else:
            join_type = "INNER"

        user_results = query_db(f"""
            SELECT *
            FROM users
            {join_type} JOIN login 
            ON users.user_id = login.user_id
            WHERE users.user_type = {user_type!r}{condition}
        """)

    current_app.logger.info(user_results)

    if user_results is None:
        return None

    return user_results


def get_username_match(username: str) -> Row | None:
    return query_db(f"""
        SELECT * 
        FROM users 
        FULL OUTER JOIN login 
        ON users.user_id = login.user_id
        WHERE login.username={username!r}
    """, single=True)


def get_user_info(user_id: int) -> Row | None:
    return query_db(f"SELECT * FROM users WHERE user_id={user_id}", single=True)


def update_user_info(
        user_id: int,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None) -> None:

    age: int | None = int(age) if age is not None else None

    modify_db(
        """
        UPDATE users set
        first_name=?,
        last_name=?,
        age=?,
        email=?,
        phone=?,
        gender=?
        WHERE user_id=?;
        """,
        first_name, last_name, age, email, phone, gender, user_id
    )


def delete_user(*, username: Optional[str] = None, user_id: Optional[int] = None) -> None:  # noqa
    """
    Deletes a user, specified by either their username or user id, from the users table.

    Keyword Arguments:
        :param username: User's username. If this is given, their id cannot be.
        :param user_id: User's id. Likewise, if this is given, their username cannot be.

    Exactly of the above keyword arguments must be provided.
    """

    raise NotImplementedError()
