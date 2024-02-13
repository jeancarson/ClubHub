from flask import Blueprint, render_template, request

from ..util.db_functions import get_users

mia_blueprint = Blueprint("mia_blueprint", __name__)


@mia_blueprint.route("/members_info")
def members_info():

    # When the user selects one of the links on the page, a HTTP GET request is sent
    # to this function with a keyword argument called selected, like:
    # "127.0.0.1:5000/members_info?selected=students"
    # And request.args contains that argument.

    selected = request.args.get("selected", None)

    if selected in ("students", "coordinators", "users"):
        user_rows = get_users(table=selected)
    else:
        user_rows = None

    return render_template('html/adminFolder/inform.html', user_rows=user_rows)


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


# @mia_blueprint.route("/profile")
# def go_profile():
#     return render_template("html/usersFolder/profile.html")  -> I had to comment this out because
#                                                                 there is another profile.html file in templates folder
#                                                                 hope u dont mind :3


@mia_blueprint.route("/clubss")  # Why is there two s's this has ruined my day Mia
def go_clubs():
    return render_template("html/usersFolder/clubss.html")


@mia_blueprint.route("/eventss")
def go_events():
    return render_template("html/usersFolder/eventss.html")
