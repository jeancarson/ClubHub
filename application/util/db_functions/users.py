from .main import (
    Optional,
    Row,
    query_db,
    modify_db,
    last_id
)
from .clubs import create_club, approve_club


def user_exists(username: str) -> bool:
    """
    Returns True if the given username exists in the database, and
    False otherwise.

    :param username: Username to check the existence of.
    """

    return query_db(f"SELECT NULL FROM login WHERE username={username!r}", single=True) is not None


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

    last_user: Row | None = last_id(table="login")
    user_id: int
    approved: str

    if last_user is None:
        user_id = 1
        user_type = "ADMINISTRATOR"
        approved = "APPROVED"  # Override approval if registration is the first on the system
    else:
        user_id = last_user["user_id"] + 1
        user_type = user_type
        approved = "PENDING"

    modify_db(
        """
            INSERT INTO users 
            (user_id, first_name, last_name, age, email, phone, gender, password, user_type, approved) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, user_id, first_name, last_name, age, email, phone, gender, password, user_type, approved
    )

    modify_db(
        """
            INSERT INTO login
            (user_id, username) VALUES
            (?, ?)
        """, user_id, username
    )

    if user_type == "COORDINATOR":
        create_club(creator_user_id=user_id, club_name=club_name, club_description=club_description)

    elif user_type == "ADMINISTRATOR":
        return True

    return False


def users_info(
        *,
        user_type: Optional[str] = None,
        pending: Optional[bool] = None,
        admin_permission: Optional[bool] = None) -> list[Row] | None:
    """
    Returns a list containing the rows from the users table, if there are any.

    Optional Keyword arguments:
        :param user_type: Should be either "STUDENT", "COORDINATOR", "ADMIN", or None (for all users).
        :param pending: If true, only includes pending (unapproved) users.
        :param admin_permission: If true, also includes username in results.
    """

    selection: str

    if admin_permission:
        selection = "*"
    else:
        selection = "first_name, last_name, age, email, phone, gender"

    results: list[Row] | None
    condition: str

    if user_type is None:
        if pending:
            condition = "WHERE users.approved='PENDING'"
        else:
            condition = ""

    else:
        condition = f"WHERE users.user_type={user_type!r}"

        if pending:
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
        "SELECT * FROM all_user_attributes WHERE username=?",
        username,
        single=True
    )


def profile_user_attributes(user_id: int) -> Row | None:
    """
    Returns all profile-related (editable) attributes of a user.

    :param user_id: User's ID.
    """
    return query_db(
        "SELECT * FROM profile_user_attributes WHERE user_id=?",
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


def get_pending_users() -> list[Row] | None:
    """
    Returns a list containing each user with an approved status of 'PENDING'.
    """

    return query_db("SELECT * FROM users WHERE approved='PENDING'")


def approve_user(user_id: int) -> None:
    """
    Approve a pending user (set approved attribute to 'APPROVED' in users table).

    :param user_id: User's ID.
    """

    user: Row | None = query_db(
        "SELECT * FROM users WHERE user_id=?",
        user_id,
        single=True
    )

    if user["user_type"] == "COORDINATOR":
        approve_club(creator_user_id=user_id)

    modify_db(
        "UPDATE users set approved='APPROVED' WHERE user_id=?",
        user_id
    )


def delete_user(user_id: int) -> None:
    """
    Deletes a user from the users & login table.

    :param user_id: User's ID.
    """

    modify_db(
        "DELETE FROM users WHERE user_id=?",
        user_id
    )

    modify_db(
        "DELETE FROM login WHERE user_id=?",
        user_id
    )
