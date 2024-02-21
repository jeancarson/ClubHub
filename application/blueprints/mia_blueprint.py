from flask import Blueprint, jsonify, render_template, request

from application.util.db_functions.main import query_db
from application.util.db_functions.clubs import count_club_memberships, insert_club_membership

mia_blueprint = Blueprint("mia_blueprint", __name__)





@mia_blueprint.route("/profile1")
def go_profile():
    return render_template("html/student/profile.html")  





@mia_blueprint.route("/studento")
def go_student():
    return render_template("html/student/student-main.html")











