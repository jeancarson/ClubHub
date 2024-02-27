from . import Optional, Row, query_db, modify_db
from .clubs import create_club, update_club_status, delete_club


def next_user_id() -> int:
    """
    Returns the next user ID.
    """

    last_user: Row | None = query_db(
        """
            SELECT user_id FROM login
            ORDER BY user_id DESC
            LIMIT 1;
        """,
        single=True
    )

    return 1 if last_user is None else last_user["user_id"] + 1


def user_exists(username: str) -> bool:
    """
    Returns True if the given username exists in the database, and
    False otherwise.

    :param username: Username to check the existence of.
    """

    result = query_db(
        """
            SELECT NULL FROM login
            WHERE username=?;
        """,
        username,
        single=True
    )

    return result is not None


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
        gender: Optional[str] = None,
        club_name: Optional[str] = None,
        club_description: Optional[str] = None) -> bool:
    """
    Creates a new user in the database.
    ID is automatically generated. Users are not approved by default.

    :return: True if user is the first on the system, False otherwise.
    """

    age: int | None = int(age) if age is not None else None

    user_id: int = next_user_id()
    approved: str

    if user_id == 1:
        user_type = "ADMINISTRATOR"
        approved = "APPROVED"  # Override approval if registration is the first on the system
    else:
        user_type = user_type
        approved = "PENDING"

    modify_db(
        """
            INSERT INTO users 
            (first_name, last_name, age, email, phone, gender, password, user_type, approved) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, first_name, last_name, age, email, phone, gender, password, user_type, approved
    )

    modify_db(
        """
            INSERT INTO login
            (user_id, username) VALUES
            (?, ?);
        """, user_id, username
    )

    if user_type == "ADMINISTRATOR":
        return True

    if user_type == "COORDINATOR":
        create_club(creator_user_id=user_id, club_name=club_name, club_description=club_description)

    return False


def users_info(
        *,
        user_type: Optional[str] = None,
        approved: Optional[bool] = None,
        admin_permission: Optional[bool] = None) -> list[Row] | None:
    """
    Returns a list containing the rows from the users table, if there are any.

    Optional Keyword arguments:
        :param user_type: Should be either "STUDENT", "COORDINATOR", "ADMIN", or None (for all users).
        :param approved: If True, returns only approved users, and if False, returns only pending users.
                         If None, then returns users regardless of status.
        :param admin_permission: If true, also includes extra user information in results.
    """

    selection: str

    if admin_permission:
        selection = "*"
    else:
        selection = "first_name, last_name, age, email, phone, gender"

    results: list[Row] | None
    condition: str

    if user_type is None:
        if approved is None:
            condition = ""
        elif approved:
            condition = "WHERE users.approved='APPROVED'"
        else:
            condition = "WHERE users.approved='PENDING'"

    else:
        condition = f"WHERE users.user_type={user_type!r}"

        if approved is None:
            pass
        elif approved:
            condition += " AND users.approved='APPROVED'"
        else:
            condition += " AND users.approved='PENDING'"

    return query_db(
        f"""
            SELECT {selection}
            FROM users
            FULL OUTER JOIN login 
            ON users.user_id = login.user_id
            {condition};
        """
    )


def all_user_attributes(username: str) -> Row | None:
    """
    Returns all attributes of a user.

    :param username: User's username.
    """

    return query_db(
        """
            SELECT * FROM all_user_attributes
            WHERE username=?;
        """,
        username,
        single=True
    )


def profile_user_attributes(user_id: int) -> Row | None:
    """
    Returns all profile-related (editable) attributes of a user.

    :param user_id: User's ID.
    """

    return query_db(
        """
            SELECT * FROM profile_user_attributes
            WHERE user_id=?;
         """,
        user_id,
        single=True
    )


def update_user_profile_info(
        user_id: int,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None) -> None:
    """
    Updates the profile information for the user with the given ID.
    """

    age: int | None = int(age) if age is not None else None

    modify_db(
        """
            UPDATE users
            SET
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


def update_user_status(user_id: int, status: str) -> None:
    """
    Update a user's status (change approved attribute).

    :param user_id: User's ID.
    :param status: New status. One of "PENDING", "APPROVED", "REJECTED".
    """

    user: Row | None = query_db(
        """
            SELECT * FROM users
            WHERE user_id=?;
        """,
        user_id,
        single=True
    )

    if user["user_type"] == "COORDINATOR":
        update_club_status(creator_user_id=user_id, status=status)

    if status == "REJECTED":
        delete_user(user_id=user_id)

    else:
        modify_db(
            """
                UPDATE users
                SET 
                    approved=?
                WHERE user_id=?;
            """,
            status,
            user_id
        )


def delete_user(user_id: int) -> None:
    """
    Deletes a user from the users & login table.

    :param user_id: User's ID.
    """

    result: Row = query_db(
        """
            SELECT user_type FROM users
            WHERE user_id=?;
        """,
        user_id,
        single=True
    )

    user_type: str = result["user_type"]

    if user_type == "COORDINATOR":
        delete_club(creator_user_id=user_id)

    modify_db(
        """
            DELETE FROM users
            WHERE user_id=?;
        """,
        user_id
    )

    modify_db(
        """
            DELETE FROM login
            WHERE user_id=?;
        """,
        user_id
    )
