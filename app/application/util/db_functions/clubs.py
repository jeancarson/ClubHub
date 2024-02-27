from typing import Optional

from . import query_db, Row, modify_db


def create_club(*, creator_user_id: int, club_name: str, club_description: Optional[str]) -> None:
    """
    Creates a new club in the database.
    ID is automatically generated. Clubs are not approved by default.

    Keyword Arguments:
        :param creator_user_id: User ID of the creator.
        :param club_name: Name of the club.

    Optional Keyword Arguments:
        :param club_description: Description for the club.
    """

    modify_db(
        """
            INSERT INTO clubs
            (club_name, club_description, creator, validity) VALUES
            (?, ?, ?, ?);    
        """, club_name, club_description, creator_user_id, 'PENDING'
    )


def update_club_status(creator_user_id: int, status: str) -> None:
    """
    Update a club's status (change approved attribute).

    :param creator_user_id: User ID of the creator.
    :param status: New status. One of "PENDING", "APPROVED", "REJECTED".
    """

    if status == "REJECTED":
        delete_club(creator_user_id=creator_user_id)

    else:
        modify_db(
            """ 
                UPDATE clubs set 
                    validity=?
                WHERE creator=?;
            """,
            status,
            creator_user_id
        )


def delete_club(creator_user_id: int) -> None:
    """
    Deletes the club with the given creator user id from the clubs table.

    :param creator_user_id: User ID of the creator.
    """

    modify_db(
        """
            DELETE FROM clubs
            WHERE creator=?;
        """, creator_user_id
    )


def is_club_member(user_id: int, club_id: int) -> None:
    """
    Returns True if the given user is registered to be a member of the
    given club and their validity status is 'APPROVED'.

    :param user_id: User's ID.
    :param club_id: Club's ID.
    """

    return query_db(
        """
            SELECT NULL FROM club_memberships
            WHERE club_id=? AND user_id=? AND validity='APPROVED';
        """, club_id, user_id
    ) is not None


def club_info(club_id: int) -> Row | None:

    return query_db(
        """
            SELECT * FROM clubs
            WHERE club_id=?;
        """, club_id, single=True
    )


def count_club_memberships(user_id: int):
    """
    Counts the number of club memberships for a given user.

    :param user_id: The ID of the user whose club memberships are being counted.
    :return: The number of club memberships for the user.
    """

    clubs_info = query_db(
        """
            SELECT COUNT(*) FROM club_memberships 
            WHERE user_id=?;
        """,
        user_id,
        single=True
    )

    return 0 if clubs_info is None else clubs_info[0]


def insert_club_membership(club_id: int, user_id: int) -> None:
    """
    Inserts a new club membership into the database.

    :param club_id: The ID of the club.
    :param user_id: The ID of the user to add as a member of the club.
    """

    modify_db(
        """
            INSERT INTO club_memberships 
            (club_id, user_id) VALUES
            (?, ?);
        """,
        club_id,
        user_id
    )

def join_club(user_id: int, club_id: int) -> None:
    """
    Adds a user to a club in the database.
    """

    modify_db(
        """
            INSERT INTO club_memberships 
            (club_id, user_id) VALUES 
            (?, ?);
        """,
        club_id,
        user_id
    )


def get_all_clubs() -> list[Row] | None:
    return query_db(
        """
            SELECT
                club_id,
                club_name,
                club_description
            FROM clubs;
        """
    )


def registered_clubs(user_id: int) -> list[Row] | None:
    """
    Returns a list of clubs that the given user has registered for,
    with either a 'PENDING' or 'APPROVED' validity.

    :param user_id: User's ID.
    """

    return query_db(
        """
            SELECT *, cm.validity as membership_status FROM clubs
            INNER JOIN club_memberships cm USING (club_id)
            WHERE cm.user_id=?;
        """, user_id
    )


def unregistered_clubs(user_id: int) -> list[Row] | None:
    """
    Returns a list of clubs that the given user has not yet registered for.

    :param user_id: User's ID.
    """

    return query_db(
        """
            SELECT *, cm.validity FROM clubs
            LEFT JOIN club_memberships cm ON clubs.club_id=cm.club_id AND cm.user_id=?
            WHERE cm.club_id IS NULL;
        """, user_id
    )
