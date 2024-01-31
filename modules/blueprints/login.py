from werkzeug import Response
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    current_app
)

from modules.general.user_auth import password_match


login = Blueprint("login", __name__)

# Temporary user dictionary with usernames/passwords for login system.
users: dict[str, str] = {
    "admin": "243262243132246f6b3835716e6a55446e50304c51675833624962347561"
             "566a53646855676179725a61777937706f726d4b73466d6f715975687a75"
}


@login.route("/login")
def login_get() -> str:
    """
    Loads the login page.
    """

    return render_template("login.html")


@login.route("/login", methods=["POST"])
def login_post() -> str | Response:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["username"]
    password: str = request.form["password"]

    if "user" in session:
        current_user: str = session["user"]
        current_app.logger.warning(f"Login fail: {current_user!r} is already logged in")
        flash(f"You are already logged in as {current_user!r}", category="error")
        return redirect("/login")

    if not username:
        current_app.logger.warning("Login fail: Empty username")
        flash("Please enter a username", category="error")
        return redirect("/login")

    if username not in users:
        current_app.logger.warning(f"Login fail: User {username!r} does not exist")
        flash(f"User {username!r} not found", category="error")
        return redirect("/login")

    hashed_pw: str = users[username]

    if not password_match(password, hashed_pw):
        current_app.logger.warning(f"Login fail: Incorrect password for user {username!r}")
        flash("Incorrect password", category="error")
        return redirect("/login")

    current_app.logger.info(f"Login success: {username!r}")
    flash(f"Successfully logged in as {username!r}", category="info")

    # Create a user session
    session["user"] = username

    return redirect("/home")
