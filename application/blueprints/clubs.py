from flask import Blueprint, redirect, render_template, request, session
from sqlite3 import Row

from ..util.authentication.alerts import success, Success, error, Error
from ..util.authentication.page_access import validate_student_perms

from application.util.db_functions.clubs import count_club_memberships,  get_all_clubs, is_club_member, join_club

clubs = Blueprint("clubs", __name__, url_prefix="/clubs")


@clubs.route("/")
def get_clubs():
    """
    Renders the clubs page.
    """

    invalid = validate_student_perms(endpoint="/clubs")

    if invalid:
        return invalid

    user_id: int = session["user-id"]


    all_clubs = get_all_clubs()

    return render_template(
        "html/student/clubs.html",
        all_clubs=all_clubs,
        is_club_member=is_club_member  
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

    # If club_id is not provided, redirect back to the clubs page
    return redirect("/clubs")




