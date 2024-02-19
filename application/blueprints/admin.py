from sqlite3 import Row

from flask import Blueprint, redirect, request, render_template, session, url_for

from application.util.db_functions.main import modify_db, query_db

from ..util.authentication.alerts import error, Error
from ..util.db_functions.users import users_info

admin = Blueprint("admin", __name__, url_prefix="/admin")


def validate_access_perms(*, endpoint: str) -> str | None:
    """
    Returns the default home page if no user is currently logged in,
    or if they do not have administrator privileges. Returns None otherwise.

    :param endpoint: Endpoint of url user wants to access.
    """

    if "user" not in session:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint=endpoint)
        return render_template("html/misc/home.html")

    user_type = session["user-type"]
    if user_type != "ADMINISTRATOR":
        error(errtype=Error.RESTRICTED_PAGE_ADMIN, endpoint=endpoint, user_type=user_type)
        return render_template("html/misc/home.html")

    return None


@admin.route("/users/info")
def users_info():
    # When the user selects one of the links on the page, a HTTP GET request is sent
    # to this function with a keyword argument called selected, like:
    # "127.0.0.1:5000/members_info?selected=students"
    # And request.args contains that argument.

    selected: str | None = request.args.get("selected", None)
    user_rows: list[Row] | None

    invalid = validate_access_perms(endpoint="/admin/users/info")

    if invalid:
        return invalid

    if selected is not None:
        selected = selected.upper()
        if selected == "ALL":
            user_rows = users_info(admin_permission=True)
        elif selected in ("COORDINATOR", "STUDENT"):
            user_rows = users_info(user_type=selected, admin_permission=True)
        else:
            user_rows = None
    else:
        user_rows = None

    return render_template('html/admin/admin-users-info.html', user_rows=user_rows)


@admin.route("/users/pending", methods=["GET", "POST"])
def users_pending():
    invalid = validate_access_perms(endpoint="/admin/users/pending")

    if invalid:
        return invalid
    
    approved_users = query_db("SELECT * FROM users WHERE approved = 'APPROVED'")
    rejected_users = query_db("SELECT * FROM users WHERE approved = 'RJEECTED'")
    pending_users = query_db("SELECT * FROM users WHERE approved = 'PENDING'")
    

    if request.method == "POST":
        user_id = request.form.get("user_id")
        action = request.form.get("action")  

        if action == "approve":
            modify_db("UPDATE users SET approved='APPROVED' WHERE user_id=?", user_id)
        elif action == "reject":
            modify_db("UPDATE users SET approved='REJECTED' WHERE user_id=?", user_id)

        #modify_db("DELETE FROM pending_users WHERE user_id=?", user_id) we could make a pending users table if needed/ move convinient (idk how to spell that)

        
        return redirect(url_for("admin.users_pending"))

    return render_template("html/admin/admin-users-pending.html")


@admin.route("/")
def admin_main():
    invalid = validate_access_perms(endpoint="/admin")

    if invalid:
        return invalid

    return render_template("html/admin/admin-main.html")


@admin.route("/approve_user", methods=["POST"])
def approve_user1():
    user_id = request.form.get("user_id")
    approve_type = request.form.get("approve_type")

    if approve_type == "Reject":
        modify_db("UPDATE users SET approved='REJECTED' WHERE user_id=?", user_id)
    else:
        modify_db("UPDATE users SET approved='APPROVED' WHERE user_id=?", user_id)

    return redirect(url_for("admin.admin_main"))


