from flask import Blueprint, render_template

mia_blueprint = Blueprint("mia_blueprint", __name__)


@mia_blueprint.route("/members_info")
def members_info():
    return render_template('html/adminFolder/inform.html')


@mia_blueprint.route("/pending_users")
def pending_users():
    return render_template("html/adminFolder/pending.html")


@mia_blueprint.route("/admin")
def admin():
    return render_template("html/adminFolder/admin_main.html")


@mia_blueprint.route("/user")
def user():
    """
    Loads the user MAIN page.
    """
    return render_template("html/usersFolder/user_main.html", header="User Page")


@mia_blueprint.route("/profile")
def go_profile():
    return render_template("html/usersFolder/profile.html")


@mia_blueprint.route("/clubss")
def go_clubs():
    return render_template("html/usersFolder/clubss.html")


@mia_blueprint.route("/eventss")
def go_events():
    return render_template("html/usersFolder/eventss.html")
