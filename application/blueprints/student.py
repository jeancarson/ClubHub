from flask import Blueprint, render_template

from application.util.db_functions import query_db
from application.util.authentication.page_access import validate_student_perms

student = Blueprint("student", __name__)


@student.route("/student-main")
def go_student():

    invalid = validate_student_perms(endpoint="/studento")

    if invalid:
        return invalid

    events_data = query_db("SELECT * FROM events")
    club_data = query_db("SELECT * FROM clubs")

    return render_template(
        "html/student/student-main.html",
        events_data=events_data,
        club_data=club_data
    )
