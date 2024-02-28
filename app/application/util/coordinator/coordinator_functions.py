"""
These functions are used to handle coordinator requests and to
interact with the database.
"""

from flask import flash

from ..db_functions import query_db, modify_db


def get_club_id(coordinator_id: int) -> int:

    result = query_db(
        """
            SELECT club_id FROM clubs
            WHERE creator=?;
        """,
        coordinator_id,
        single=True
    )

    return result["club_id"]


def get_coordinator_name(club_id: int) -> str:

    result = query_db(
        """
            SELECT users.first_name, users.last_name
            FROM users 
            JOIN clubs ON users.user_id = clubs.creator
            WHERE clubs.club_id=?;
        """,
        club_id,
        single=True
    )

    return f"{result['first_name']} {result['last_name']}"


def get_club_details(club_id: int) -> tuple[str, str]:

    club_details = query_db(
        """
            SELECT club_name, club_description
            FROM clubs
            WHERE club_id=?;
        """,
        club_id,
        single=True
    )

    club_name = club_details["club_name"]
    club_description = club_details["club_description"]

    return club_name, club_description


def save_club_details(club_id: int, new_name: str, new_description: str) -> None:

    modify_db(
        """
            UPDATE clubs
            SET
                club_name=?,
                club_description=?
            WHERE club_id=?;
        """,
        new_name,
        new_description,
        club_id
    )

    flash("Club details successfully updated", "info")


# --------------------- Viewing members and participants ---------------------


def count_active_users(club_id: int) -> int:

    number_of_active_users = query_db(
        """
            SELECT COUNT(user_id) FROM club_memberships
            WHERE club_id=? and validity='APPROVED';
        """,
        club_id,
        single=True
    )

    return number_of_active_users[0]


def count_pending_users(club_id: int) -> int:

    number_of_pending_users = query_db(
        """
            SELECT COUNT(user_id) FROM club_memberships
            WHERE club_id=? and validity='PENDING';
        """,
        club_id,
        single=True
    )

    return number_of_pending_users[0]


# To get a list of all members of a certain status (approved/pending)
def get_all_members(club_id, status):

    status_users = query_db(
        """
            SELECT users.* FROM users
            JOIN club_memberships USING (user_id)
            WHERE club_memberships.validity=? and club_memberships.club_id=?;
        """,
        status.upper(),
        club_id
    )

    return status_users


# Save members after changing their status
def save_member_status(club_id, user_id, new_validity):

    modify_db(
        """
            UPDATE club_memberships
            SET validity=?
            WHERE user_id=? and club_id=?;
        """,
        new_validity.upper(),
        user_id,
        club_id
    )


# This will be run immediately after the save_member_status function, to get rid of the rejected members
def delete_rejected_members(club_id):

    modify_db(
        """
            DELETE FROM club_memberships
            WHERE validity='REJECTED' AND club_id=?
        """,
        club_id
    )


# --------------------- Viewing Events ---------------------


# View a small number of events straight on the dashboard
def limited_view_all_upcoming_events(club_id):

    return query_db(
        """
            SELECT * FROM events
            WHERE club_id=? AND datetime(date || ' ' || time) >= CURRENT_TIMESTAMP
            ORDER BY date
            LIMIT 5;
        """,
        club_id
    )


def count_pending_participants(event_id: int) -> int:

    result = query_db(
        """
            SELECT COUNT(user_id) FROM event_participants
            WHERE event_id=? AND validity='PENDING';
        """,
        event_id,
        single=True
    )

    return result[0]


def count_approved_participants(event_id: int) -> int:

    result = query_db(
        """
            SELECT COUNT(user_id) FROM event_participants
            WHERE event_id=? AND validity='APPROVED';
        """,
        event_id,
        single=True
    )

    return result[0]


# Retreive all participants for a particular event, who are of a certain status
def get_all_participants(event_id, status):

    return query_db(
        """
            SELECT users.* FROM users
            JOIN event_participants USING (user_id)
            WHERE event_participants.validity=? AND event_participants.event_id=?;
        """,
        status.upper(),
        event_id
    )


# Similarly to the save members functon, this function will save the status
# of the participants after it has been changed
# Deleting the rejected participants will be done immediately after this function
def save_participant_status(event_id, user_id, new_validity):

    modify_db(
        """
            UPDATE event_participants
            SET
                validity=?,
                updated=CURRENT_TIMESTAMP
            WHERE user_id=? AND event_id=?;
        """,
        new_validity.upper(),
        user_id,
        event_id
    )


def delete_rejected_participants(event_id):

    modify_db(
        """
            DELETE FROM event_participants
            WHERE validity='REJECTED' AND event_id=?;
        """,
        event_id
    )


# View all past/upcoming events
def view_all_events(club_id, timeline):

    if timeline == 'Past':
        return query_db(
            """
                SELECT * FROM events
                WHERE club_id=? AND datetime(date || ' ' || time) < CURRENT_TIMESTAMP
                ORDER BY date, time DESC;
            """,
            club_id
        )

    return query_db(
        """
            SELECT * FROM events
            WHERE club_id=? and datetime(date || ' ' || time) >= CURRENT_TIMESTAMP
            ORDER BY date, time DESC;
        """,
        club_id
    )

                                    
# --------------------- Editing Events ---------------------


# Retrieving event details to be displayed in the form
def get_event_details(event_id):

    return query_db(
        """
            SELECT * FROM events
            WHERE event_id=?;
        """,
        event_id,
        single=True
    )


def add_event(club_id, event_name, event_description, event_date, event_time, event_location):

    modify_db(
        """
            INSERT INTO events (club_id, event_name, event_description, date, time, venue)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
        club_id,
        event_name,
        event_description,
        event_date,
        event_time,
        event_location
    )


def update_event(event_id, event_name, event_description, event_date, event_time, event_location):

    modify_db(
        """
            UPDATE events
            SET 
                event_name=?,
                event_description=?,
                venue=?
                date=?,
                time=?,
                updated=CURRENT_TIMESTAMP
            WHERE event_id=?;
        """,
        event_name,
        event_description,
        event_location,
        event_date,
        event_time,
        event_id
    )
