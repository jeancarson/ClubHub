from flask import Blueprint, redirect, render_template, request, session
from sqlite3 import Row

from ..util.authentication.alerts import success, Success, error, Error
from ..util.authentication.page_access import validate_student_perms
from ..util.db_functions.clubs import (
    count_club_memberships,
    join_club,
    registered_clubs,
    unregistered_clubs
)

clubs = Blueprint("clubs", __name__, url_prefix="/clubs")


@clubs.route("/")
def get_clubs():
    """
    Renders the clubs page.
    """

    invalid = validate_student_perms(endpoint="/clubs")

    if invalid:
        return invalid

    selected: str | None = request.args.get("selected", None)
    clubs: list[Row] | None

    user_id: int = session["user-id"]
    registered: list[Row] | None = registered_clubs(user_id=user_id)
    unregistered: list[Row]

    if selected == "popular":
        unregistered = unregistered_clubs(user_id=user_id)[:5]
    else:
        unregistered = unregistered_clubs(user_id=user_id)

    return render_template(
        "html/student/clubs.html",
        unregistered=unregistered,
        registered=registered,
        selected_view=selected
    )


@clubs.route("/join", methods=["POST"])
def join_club_route():

    invalid = validate_student_perms(endpoint="/join")

    if invalid:
        return invalid

    user_id: int = session["user-id"]
    username: str = session["user"]

    club_id: str | None = request.args.get("club_id", None)
    club_name: str | None = request.args.get("club_name", None)

    if club_id is not None and club_name is not None:
        if count_club_memberships(user_id) >= 3:
            error(
                endpoint="/clubs/join",
                errtype=Error.CLUB_TRESHOLD_REACHED,
                form=True,
                username=username
            )
        else:
            success(
                endpoint="/clubs/join",
                successtype=Success.CLUB_REGISTER,
                form=True,
                username=username,
                club_id=club_id,
                club_name=club_name
            )

            join_club(user_id, club_id)

    return redirect("/clubs")