
from flask import Blueprint, redirect, render_template, request, session
from application.util.authentication.alerts import Success, success
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
def join_club_action() -> str:
    invalid = validate_student_perms(endpoint="/clubs/join")

    if invalid:
        return invalid

    user_id: int = session["user-id"]
    club_id = request.args.get("club_id")

    if club_id is not None:
        if is_club_member(user_id, int(club_id)):
           
            return redirect("/clubs?joined=true")
        else:
            # Check if the user has reached the membership limit
            memberships_count = count_club_memberships(user_id)
            if memberships_count >= 3:
                # User has already joined three clubs
                return redirect("/clubs?limit_reached=true")
            else:
                # Attempt to join the club
                if join_club(user_id=user_id, club_id=int(club_id)):
                    # User successfully joined the club
                    return redirect("/clubs?joined=true")
                else:
                    # User couldn't join due to membership limit reached
                    return redirect("/clubs?limit_reached=true")

    # If club_id is not provided, redirect back to the clubs page
    return redirect("/clubs")




