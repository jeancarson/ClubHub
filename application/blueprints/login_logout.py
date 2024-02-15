from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    url_for,
    redirect,
    current_app
)
from werkzeug import Response

from ..util.db_functions import query_db
from ..util.authentication import current_user, current_user_info, login, logout
from ..util.authentication.alerts import error, success, Error, Success
from ..util.authentication.passwords import password_match

login_logout: Blueprint = Blueprint("login_logout", __name__)


@login_logout.route("/login")
def login_get() -> Response | str:
    """
    Loads the login page.
    """

    form_username_value: str = request.args.get("username", "")
    user: str | None = current_user()

    if user is not None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_IN, endpoint="/login", user=user)
        return redirect("/profile")

    return render_template("html/auth/login.html", form_username_value=form_username_value)


@login_logout.route("/login", methods=["POST"])
def login_post() -> Response | str:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["login-username"]
    password: str = request.form["login-password"]

    match = query_db(f"SELECT * FROM login WHERE username={username!r}", single=True)

    if match is None:
        current_app.logger.info(f"[page='/login' (FORM)] => Invalid username")
        flash(f"User not found: {username!r} ", category="error")
        return redirect("/login")

    if not password_match(password, match["password"]):
        current_app.logger.info(f"[page='/login' (FORM)] => Incorrect password")
        flash("Incorrect password", category="error")
        return redirect(url_for(".login_get", username=username))

    if match["approved"] != "APPROVED":
        current_app.logger.info(f"[page='/login' (FORM)] => Account still awaiting administrator approval")
        flash("Your account is awaiting administrator approval", category="error")
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
        session.pop("user", None)

    return redirect("/home")
