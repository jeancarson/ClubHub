from flask import Blueprint, render_template, request

from application.util.db_functions.main import query_db


mia_blueprint = Blueprint("mia_blueprint", __name__)






@mia_blueprint.route("/studento")
def go_student():
    events_data = query_db("SELECT * FROM events")
    club_data = query_db("SELECT * FROM clubs")
    return render_template("html/student/student-main.html", events_data=events_data, club_data=club_data)











