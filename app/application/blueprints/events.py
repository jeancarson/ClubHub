from flask import Blueprint, render_template, session, request
from sqlite3 import Row

from ..util.authentication.alerts import success, Success
from ..util.authentication.page_access import validate_student_perms
from ..util.db_functions.events import registered_events, unregistered_events, register_for_event
from ..util.db_functions.clubs import club_info

events = Blueprint("events", __name__, url_prefix="/events")


@events.route("/")
def events_main() -> str:

    invalid = validate_student_perms(endpoint="/events")

    if invalid:
        return invalid

    user_id: int = session["user-id"]

    return render_template(
        "html/student/events.html",
        registered=registered_events(user_id=user_id),
        unregistered=unregistered_events(user_id=user_id)
    )


@events.route("/club-info")
def events_club_info() -> str:

    invalid = validate_student_perms(endpoint="/events")

    if invalid:
        return invalid

    club_id = request.args.get("club_id", None)

    if club_id is not None:
        club_information: Row | None = club_info(club_id=int(club_id))

        if club_information:
            return render_template("html/student/club-info.html", club_information=club_information)

    user_id: int = session["user-id"]

    return render_template(
        "html/student/events.html",
        registered=registered_events(user_id=user_id),
        unregistered=unregistered_events(user_id=user_id)
    )


@events.route("/register", methods=["POST"])
def events_register() -> str:

    invalid = validate_student_perms(endpoint="/events/register")

    if invalid:
        return invalid

    user_id: int = session["user-id"]

    event_id = request.args.get("event_id", None)
    event_name = request.args.get("event_name", None)
    club_id = request.args.get("club_id", None)

    if event_id is not None and event_name is not None:
        is_member: bool = register_for_event(
            user_id=user_id,
            event_id=int(event_id),
            club_id=int(club_id)
        )

        username: str = session["user"]

        if is_member:
            success(
                successtype=Success.EVENT_REGISTER_APPROVED, endpoint="/events/register",
                username=username,
                event_id=event_id,
                event_name=event_name
            )
        else:
            success(
                successtype=Success.EVENT_REGISTER_PENDING, endpoint="/events/register",
                username=username,
                event_id=event_id,
                event_name=event_name
            )

    return render_template(
        "html/student/events.html",
        registered=registered_events(user_id=user_id),
        unregistered=unregistered_events(user_id=user_id)
    )
