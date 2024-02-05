from werkzeug import Response
from flask import (
    Blueprint,
    render_template,
    session,
    flash,
    redirect,
    request,
    url_for
)

registration = Blueprint("registration", __name__)


def validate_password(password: str) -> None | str:

    errors: list[str] = []
    error_msg_prefix: str = "Password must contain"
    error_msg: str

    lower: bool = False
    upper: bool = False
    digit: bool = False

    for char in password:
        code: int = ord(char)

        if code in range(65, 91):
            upper = True
        elif code in range(97, 122):
            lower = True
        else:
            digit = True

    if not upper:
        errors.append("a lowercase character")
    if not lower:
        errors.append("an uppercase character")
    if not digit:
        errors.append("a digit")

    if not errors:
        return None

    if len(errors) == 1:
        error_msg = errors[0]
    elif len(errors) == 2:
        error_msg_prefix += ":"
        error_msg = f"{errors[0]} and {errors[1]}"
    else:
        error_msg_prefix += ":"
        error_msg = f"{errors[0]}, {errors[1]}, and {errors[2]}"

    return f"{error_msg_prefix} {error_msg}"


@registration.route("/register")
def register_get() -> Response | str:
    """
    Loads the registration page.
    """

    form_username: str = request.args.get("username", "")
    form_name: str = request.args.get("name", "")
    form_email: str = request.args.get("email", "")

    if "user" in session:
        flash("You must log out before creating a new account", category="error")
        return redirect("/profile")

    return render_template(
        "register.html",
        form_username_value=form_username,
        form_name_value=form_name,
        form_email_value=form_email
    )


@registration.route("/register", methods=["POST"])
def register_post() -> Response:

    username: str = request.form["register-username"]
    password: str = request.form["register-password"]
    confirm_password: str = request.form["register-confirm-password"]
    name: str = request.form["register-name"]
    email: str = request.form["register-email"]

    # TODO: Check if username in registered users already

    password_error_msg: None | str = validate_password(password)

    if password_error_msg:
        flash(password_error_msg, category="error")
        return redirect(url_for(".register_get", username=username, name=name, email=email))

    if confirm_password != password:
        flash("Passwords do not match", category="error")
        return redirect(url_for(".register_get", username=username, name=name, email=email))

    # TODO: Create a new account
    flash(f"Register success: {username!r}", category="info")

    # Create a user session
    session["user"] = username

    return redirect("/profile")
