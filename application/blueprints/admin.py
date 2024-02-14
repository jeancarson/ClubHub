from sqlite3 import Row

from flask import Blueprint, request, render_template

from ..util.db_functions import get_users_info

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/users/info")
def users_info():
    # When the user selects one of the links on the page, a HTTP GET request is sent
    # to this function with a keyword argument called selected, like:
    # "127.0.0.1:5000/members_info?selected=students"
    # And request.args contains that argument.

    selected: str | None = request.args.get("selected", None)
    user_rows: list[Row] | None

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
    return render_template("html/admin/admin-users-pending.html")


@admin.route("/")
def admin_main():
    return render_template("html/admin/admin-main.html")
