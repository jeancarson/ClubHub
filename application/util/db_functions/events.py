from typing import Optional

from .main import Row, query_db, modify_db


def registered_event_ids(user_id: int, as_string: Optional[bool] = None) -> tuple[str, ...] | str | None:
    """
    Returns a tuple containing all event ids (as strings) for events
    that the given user is registered for.

    :param user_id: User's ID.
    :param as_string: If True, returns a string representation of the tuple (to be used in a query).
    """

    rows: list[Row] | None = query_db(
        """
            SELECT event_id 
            FROM event_participants
            WHERE user_id=?
        """, user_id
    )

    if rows is None:
        return None

    tup: tuple[str, ...] = tuple(str(row["event_id"]) for row in rows)

    if as_string:
        return f"({', '.join(tup)})"  # Rather than returning str(tup), as that may contain a trailing comma

    return tup


def unregistered_events(user_id: int) -> list[Row] | None:
    """
    Returns a list of events that the given user is not registered for.

    :param user_id: User's ID.
    """

    # Add trigger to removed expired events?

    registered_ids: str | None = registered_event_ids(user_id=user_id, as_string=True)
    where_condition: str

    if registered_ids is None:
        where_condition = ";"
    else:
        where_condition = f"WHERE events.event_id NOT IN {registered_ids};"

    return query_db(
        f"""
            SELECT * 
            FROM events
            FULL OUTER JOIN CLUBS 
            ON events.club_id = clubs.club_id
            {where_condition}
        """
    )


def registered_events(user_id: int) -> list[Row] | None:
    """
    Returns a list of events that the given user is registered for.

    :param user_id: User's ID.
    """

    registered_ids: str | None = registered_event_ids(user_id=user_id, as_string=True)

    if registered_ids is None:
        return None

    return query_db(
        f"""
            SELECT * 
            FROM events
            FULL OUTER JOIN CLUBS 
            ON events.club_id = clubs.club_id
            WHERE events.event_id IN {registered_ids};
        """
    )


def register_for_event(user_id: int, event_id: int | str) -> None:
    """
    Registers a user for an event.

    :param user_id: User's ID.
    :param event_id: Event's ID.
    """

    event_id: str = str(event_id) if isinstance(event_id, int) else event_id

    # TODO: Check club membership
    validity: str = "APPROVED"

    # TODO: Make these function calls more efficient?
    registered_ids: str | None = registered_event_ids(user_id=user_id)
    print(registered_ids)

    if registered_ids is not None:
        if event_id in registered_ids:
            return None

    modify_db(
        """
            INSERT INTO event_participants
            (event_id, user_id, validity) VALUES
            (?, ?, ?)
        """, event_id, user_id, validity
    )
