from typing import Optional

from . import query_db
from .main import Row, last_id, modify_db
from .. import get_current_timestamp


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

    last_club: Row | None = last_id(table="clubs")
    club_id: int

    if last_club is None:
        club_id = 1
    else:
        club_id = last_club["club_id"] + 1

    modify_db(
        """
            INSERT INTO clubs
            (club_id, club_name, club_description, creator, validity) VALUES
            (?, ?, ?, ?, ?)
        """, club_id, club_name, club_description, creator_user_id, 'PENDING'
    )


def approve_club(creator_user_id: int) -> None:
    """
    Approve a pending club (set approved attribute to 'APPROVED' in clubs table).

    :param creator_user_id: User ID of the creator.
    """

    timestamp: str = get_current_timestamp()

    modify_db(
        """ 
            UPDATE clubs set 
                validity='APPROVED',
                updated=?
            WHERE creator=?
        """, timestamp, creator_user_id
    )


def delete_club(creator_user_id: int) -> None:
    """
    Deletes the club with the given creator user id from the clubs table.

    :param creator_user_id: User ID of the creator.
    """

    modify_db(
        """
            DELETE FROM clubs
            WHERE creator=?
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
            WHERE club_id=? AND user_id=? AND validity='APPROVED'
        """, club_id, user_id
    ) is not None


def club_info(club_id: int) -> Row | None:

    return query_db(
        """
        SELECT * from clubs
        WHERE club_id=?
        """, club_id, single=True
    )


def count_club_memberships(user_id):
    clubs_info = query_db("SELECT COUNT(*) FROM club_memberships WHERE user_id = ?", (user_id,))
    return clubs_info[0]['COUNT(*)'] if clubs_info else 0


def insert_club_membership(club_id, user_id):
    query_db("INSERT INTO club_memberships (club_id, user_id) VALUES (?, ?)", (club_id, user_id))
