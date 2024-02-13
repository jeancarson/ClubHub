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

from ..util.db_functions import query_db, user_approved
from ..util.user_auth import password_match

login_logout: Blueprint = Blueprint("login_logout", __name__)


@login_logout.route("/login")
def login_get() -> Response | str:
    """
    Loads the login page.
    """

    form_username_value: str = request.args.get("username", "")

    if "user" in session:
        current_user: str = session["user"]
        current_app.logger.info(f"[page='/login'] => Authenticated user tried to access restricted page")
        flash(f"You are already logged in as {current_user!r}", category="error")
        return redirect("/profile")

    return render_template("html/auth/login.html", form_username_value=form_username_value)


@login_logout.route("/login", methods=["POST"])
def login_post() -> Response | str:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["login-username"]
    password: str = request.form["login-password"]

    match = query_db(f"SELECT password FROM users WHERE username='{username}'", single=True)

    if match is None:
        current_app.logger.info(f"[page='/login' (FORM)] => Invalid username")
        flash(f"User {username!r} not found", category="error")
        return redirect("/login")

    if not password_match(password, match["password"]):
        current_app.logger.info(f"[page='/login' (FORM)] => Incorrect password")
        flash("Incorrect password", category="error")
        return redirect(url_for(".login_get", username=username))

    if not user_approved(username=username):
        current_app.logger.info(f"[page='/login' (FORM)] => Account still awaiting administrator approval")
        flash("Your account is awaiting administrator approval", category="error")
        return redirect("/home")

    current_app.logger.info(f"[page='/login' (FORM)] => Login successful for user: {username!r}")
    flash(f"Successfully logged in as {username!r}", category="info")

    # Create a user session
    session["user"] = username

    return redirect("/profile")


@login_logout.route("/logout")
def logout() -> Response:
    """
    Logs out of the current session (if any) and redirects to home page.
    """

    if "user" in session:
        username: str = session["user"]
        current_app.logger.info(f"[page='/logout'] => Logout successful for user: {username!r}")
        flash(f"You have been logged out. See you later {username!r}!", category="info")
        session.pop("user", None)
    else:
        flash("You can not log out if you are not logged in!", category="error")

    return redirect("/home")


@login_logout.route("/profile")
def profile() -> str | Response:
    """
    Loads the account page (if a user session is active).
    """

    if "user" not in session:
        current_app.logger.info(f"[page='/profile'] => Unauthenticated user tried to access restricted page")
        flash("You cannot access this page as you are not logged in", category="error")
        return redirect("/home")

    return render_template("html/profile.html", user=session["user"])


@login_logout.route("/forgot-password")
def forgot_password() -> str:
    """
    Loads the forgot password page.
    """

    return render_template("html/auth/forgot-password.html")
