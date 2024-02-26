from sqlite3 import Row

from flask import Blueprint, redirect, request, render_template

from ..util.authentication.alerts import success, Success
from ..util.authentication.page_access import validate_admin_perms
from ..util.db_functions.users import users_info, update_user_status

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/users/info")
def users_information() -> str:

    invalid = validate_admin_perms(endpoint="/admin/users/info")

    if invalid:
        return invalid

    selected: str | None = request.args.get("selected", None)
    user_rows: list[Row] | None

    if selected is not None:
        selected = selected.upper()

    if selected in ("COORDINATOR", "STUDENT"):
        user_rows = users_info(user_type=selected, admin_permission=True)
    else:
        user_rows = users_info(admin_permission=True)

    return render_template(
        'html/admin/users-info.html',
        user_rows=user_rows
    )


@admin.route("/users/pending")
def users_pending():

    invalid = validate_admin_perms(endpoint="/admin/users/pending")

    if invalid:
        return invalid
    
    approved_users: list[Row] | None = users_info(approved=True, admin_permission=True)
    pending_users: list[Row] | None = users_info(approved=False, admin_permission=True)

    return render_template(
        "html/admin/pending-users.html",
        approved_users=approved_users,
        pending_users=pending_users
    )


@admin.route("/users/pending", methods=["POST"])
def users_pending_post():

    user_id: str = request.form.get("user_id")
    action: str = request.form.get("action")

    try:
        user_id: int = int(user_id)
    except ValueError:
        pass
    else:
        if action == "approve":
            update_user_status(user_id=user_id, status="APPROVED")
            success(
                endpoint="/admin/users/pending",
                successtype=Success.USER_APPROVED,
                form=True,
                user_id=user_id
            )
        elif action == "reject":
            update_user_status(user_id=user_id, status="REJECTED")
            success(
                endpoint="/admin/users/pending",
                successtype=Success.USER_REJECTED,
                form=True,
                user_id=user_id
            )

    return redirect("/admin/users/pending")
