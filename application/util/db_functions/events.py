from . import Row, query_db, modify_db
from .clubs import is_club_member


def get_all_events() -> list[Row] | None:
    return query_db("SELECT * FROM events;")


def registered_events(user_id: int) -> list[Row] | None:
    """
    Returns a list of events that the given user has registered for,
    with either a 'PENDING' or 'APPROVED' validity.

    :param user_id: User's ID.
    """

    return query_db(
        """
            SELECT *, ep.validity FROM event_info
            INNER JOIN event_participants ep USING (event_id)
            WHERE ep.user_id=?;
        """, user_id
    )


def unregistered_events(user_id: int) -> list[Row] | None:
    """
    Returns a list of events that the given user has not yet registered for.

    :param user_id: User's ID.
    """

    return query_db(
        """
            SELECT *, ep.validity FROM event_info
            LEFT JOIN event_participants ep ON event_info.event_id=ep.event_id AND ep.user_id=?
            WHERE ep.event_id IS NULL;
        """, user_id
    )


def register_for_event(user_id: int, event_id: int, club_id: int) -> bool:
    """
    Registers a user for an event.

    :param user_id: User's ID.
    :param event_id: Event's ID.
    :param club_id: ID of the club hosting the event.

    :return: True if user is a club member, False otherwise.
    """

    validity: str
    retval: bool

    if is_club_member(user_id=user_id, club_id=club_id):
        validity = "APPROVED"
        retval = True
    else:
        validity = "PENDING"
        retval = False

    modify_db(
        """
            INSERT INTO event_participants
            (event_id, user_id, validity) VALUES
            (?, ?, ?);
        """, event_id, user_id, validity
    )

    return retval
