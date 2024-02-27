from flask import Blueprint, render_template

from ..util.authentication.page_access import validate_student_perms
from ..util.db_functions.clubs import get_all_clubs
from ..util.db_functions.events import get_all_events

student = Blueprint("student", __name__)


@student.route("/student-dashboard")
def go_student():
    invalid = validate_student_perms(endpoint="/student-main")

    if invalid:
        return invalid

    return render_template(
        "html/student/student-main.html",
        events_data=get_all_events(),
        club_data=get_all_clubs()
    )
