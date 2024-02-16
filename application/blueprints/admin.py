from sqlite3 import Row

from flask import Blueprint, request, render_template, session

from ..util.authentication.alerts import error, Error
from ..util.db_functions import get_users_info

admin = Blueprint("admin", __name__, url_prefix="/admin")


def validate_access_perms(*, endpoint: str) -> str | None:
    """
    Returns the default home page if no user is currently logged in,
    or if they do not have administrator privileges. Returns None otherwise.

    :param endpoint: Endpoint of url user wants to access.
    """

    if "user" not in session:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint=endpoint)
        return render_template("html/misc/default-home.html")

    user_type = session["user-type"]
    if user_type != "ADMINISTRATOR":
        error(errtype=Error.RESTRICTED_PAGE_ADMIN, endpoint=endpoint, user_type=user_type)
        return render_template("html/misc/default-home.html")

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
            user_rows = get_users_info(admin_permission=True)
        elif selected in ("COORDINATOR", "STUDENT"):
            user_rows = get_users_info(user_type=selected, admin_permission=True)
        else:
            user_rows = None
    else:
        user_rows = None

    return render_template('html/admin/admin-users-info.html', user_rows=user_rows)


@admin.route("/users/pending")
def users_pending():
    invalid = validate_access_perms(endpoint="/admin/users/pending")

    if invalid:
        return invalid

    return render_template("html/admin/admin-users-pending.html")


@admin.route("/")
def admin_main():
    invalid = validate_access_perms(endpoint="/admin")

    if invalid:
        return invalid

    return render_template("html/admin/admin-main.html")
