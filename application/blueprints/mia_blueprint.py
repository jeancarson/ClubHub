from flask import Blueprint, render_template, request

from ..util.db_functions import get_users

mia_blueprint = Blueprint("mia_blueprint", __name__)


@mia_blueprint.route("/member-info")
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

    return render_template('html/admin/inform.html', user_rows=user_rows)


@mia_blueprint.route("/pending-users")
def pending_users():
    return render_template("html/admin/pending.html")


@mia_blueprint.route("/admin")
def admin():
    return render_template("html/admin/admin-main.html")


@mia_blueprint.route("/user")
def user():
    """
    Loads the user MAIN page.
    """
    return render_template("html/student/student-main.html", header="User Page")


# @mia_blueprint.route("/profile")
# def go_profile():
#     return render_template("html/student/profile.html")  -> I had to comment this out because
#                                                                 there is another profile.html file in templates folder
#                                                                 hope u dont mind :3


@mia_blueprint.route("/clubs")
def go_clubs():
    return render_template("html/student/clubs.html")


@mia_blueprint.route("/events")
def go_events():
    return render_template("html/student/events.html")
