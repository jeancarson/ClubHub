from werkzeug import Response
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    url_for,
    redirect
)

from ..util.database import query_db
from ..util.user_auth import password_match


login_logout: Blueprint = Blueprint("login_logout", __name__)

# TODO: Remove this
# # Temporary user dictionary with usernames/passwords for login system.
# users: dict[str, str] = {
#     "admin": "243262243132246f6b3835716e6a55446e50304c51675833624962347561"
#              "566a53646855676179725a61777937706f726d4b73466d6f715975687a75"
# }


@login_logout.route("/login")
def login_get() -> Response | str:
    """
    Loads the login page.
    """

    form_username_value: str = request.args.get("username", "")

    if "user" in session:
        current_user: str = session["user"]
        flash(f"You are already logged in as {current_user!r}", category="error")
        return redirect("/profile")

    return render_template("html/login.html", form_username_value=form_username_value)


@login_logout.route("/login", methods=["POST"])
def login_post() -> Response | str:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["login-username"]
    password: str = request.form["login-password"]

    match = query_db(f"SELECT password FROM users WHERE username='{username}'", single=True)

    if match is None:
        flash(f"User {username!r} not found", category="error")
        return redirect("/login")

    if not password_match(password, match["password"]):
        flash("Incorrect password", category="error")
        return redirect(url_for(".login_get", username=username))

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
        flash(f"You have been logged out. See you later {session['user']}!", category="info")
        session.pop("user", None)
    else:
        flash("You can not log out if you are not logged in!", category="error")

    return redirect("/home")


@login_logout.route("/profile")
def profile() -> str | Response:
    """
    Loads the account page (if a user session is active)
    """

    if "user" not in session:
        flash("You cannot access this page as you are not logged in", category="error")
        return redirect("/home")

    return render_template("html/profile.html", user=session["user"])


@login_logout.route("/forgot-password")
def forgot_password() -> str:
    """
    Loads the forgot password page.
    """

    return render_template("html/forgot-password.html")
