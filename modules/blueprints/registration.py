from werkzeug import Response
from flask import (
    Blueprint,
    render_template,
    session,
    flash,
    redirect,
    current_app
)


registration = Blueprint("registration", __name__)


@registration.route("/register")
@registration.route("/registration")
@registration.route("/create-account")
@registration.route("/sign-up")
def register_get() -> Response | str:
    """
    Loads the registration page.
    """

    if "user" in session:
        current_app.logger.warning(f"Page access fail: authenticated user tried to access restricted page 'register'")
        flash("You must log out before creating a new account", category="error")
        return redirect("/account")

    return render_template("register.html")
