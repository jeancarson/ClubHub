from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
)
from werkzeug import Response

from ..util.authentication import current_user, login, logout
from ..util.authentication.alerts import error, success, Error, Success
from ..util.authentication.passwords import password_match
from ..util.db_functions.users import all_user_attributes

login_logout: Blueprint = Blueprint("login_logout", __name__)


@login_logout.route("/login")
def login_get() -> Response | str:
    """
    Loads the login page.
    """

    user: str | None = current_user()
    print(user)

    if user is not None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_IN, endpoint="/login", user=user)
        return redirect("/profile")

    form_username_value: str = request.args.get("username", "")

    return render_template("html/auth/login.html", form_username_value=form_username_value)


@login_logout.route("/login", methods=["POST"])
def login_post() -> Response | str:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["login-username"]
    password: str = request.form["login-password"]

    match = all_user_attributes(username=username)

    if match is None:
        error(errtype=Error.INVALID_USERNAME, endpoint="/register", form=True, username=username)
        return redirect("/login")

    if not password_match(password, match["password"]):
        error(errtype=Error.INCORRECT_PW, endpoint="/login", form=True, username=username)
        return redirect(url_for(".login_get", username=username))

    if match["approved"] != "APPROVED":
        error(errtype=Error.UNAPPROVED, endpoint="/login", form=True, username=username)
        return redirect("/home")

    user_id: int = match["user_id"]
    user_type: str = match["user_type"]

    login(user_id=user_id, username=username, user_type=user_type)
    success(successtype=Success.LOGIN, endpoint="/login", form=True, username=username, user_type=user_type)

    return redirect("/profile")


@login_logout.route("/logout")
def logout_get() -> Response:
    """
    Logs out of the current session (if any) and redirects to home page.
    """

    user: str | None = current_user()

    if user is None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint="/logout")
    else:
        logout()
        success(successtype=Success.LOGOUT, endpoint="/logout", user=user)

    return redirect("/home")
