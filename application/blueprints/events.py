from flask import Blueprint, render_template, session, request

from ..util.authentication.alerts import error, Error, success, Success
from ..util.db_functions.events import registered_events, unregistered_events, register_for_event

events = Blueprint("events", __name__, url_prefix="/events")


def validate_access_perms(*, endpoint: str) -> str | None:
    """
    Returns the default home page if no user is currently logged in,
    or if they do not have student privileges. Returns None otherwise.

    :param endpoint: Endpoint of url user wants to access.
    """

    if "user" not in session:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint=endpoint)
        return render_template("html/misc/home.html")

    user_type = session["user-type"]
    if user_type != "STUDENT":
        error(errtype=Error.RESTRICTED_PAGE_STUDENT, endpoint=endpoint, user_type=user_type)
        return render_template("html/misc/home.html")

    return None


@events.route("/")
def events_main():
    invalid = validate_access_perms(endpoint="/events")

    if invalid:
        return invalid

    user_id: int = session["user-id"]

    return render_template(
        "html/student/events.html",
        registered=registered_events(user_id=user_id),
        unregistered=unregistered_events(user_id=user_id)
    )


@events.route("/register")
def events_register():

    invalid = validate_access_perms(endpoint="/events/register")

    if invalid:
        return invalid

    user_id: int = session["user-id"]

    event_id = request.args.get("event_id", None)
    event_name = request.args.get("event_name", None)

    if event_id is not None and event_name is not None:
        register_for_event(user_id=user_id, event_id=int(event_id))
        username: str = session["user"]

        success(
            successtype=Success.EVENT_REGISTER, endpoint="/events/register",
            username=username,
            event_id=event_id,
            event_name=event_name
        )

    return render_template(
        "html/student/events.html",
        registered=registered_events(user_id=user_id),
        unregistered=unregistered_events(user_id=user_id)
    )
