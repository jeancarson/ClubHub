from flask import Blueprint, render_template

mia_blueprint = Blueprint("mia_blueprint", __name__)


@mia_blueprint.route("/user")
def user():
    """
    Loads the user MAIN page.
    """
    return render_template("html/student/student-main.html", header="User Page")


@mia_blueprint.route("/profile1")
def go_profile():
    return render_template("html/student/profile.html")  


@mia_blueprint.route("/clubs")
def go_clubs():
    return render_template("html/student/clubs.html")


@mia_blueprint.route("/events")
def go_events():
    return render_template("html/student/events.html")
