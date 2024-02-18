from typing import Optional

from .main import Row, last_id, modify_db
from .. import get_current_timestamp


def create_club(*, creator_user_id: int, club_name: str, club_description: Optional[str]) -> None:
    """
    Creates a new club in the database.
    ID is automatically generated. Clubs are not approved by default.

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
            WHERE user_id=?
        """, creator_user_id
    )
