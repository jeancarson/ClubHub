from flask import (
    Blueprint,
    render_template,
    session,
    flash,
    redirect,
    request,
    url_for,
current_app
)
from werkzeug import Response

# '..' means parent directory
from ..util.db_functions import user_exists, create_user
from ..util.user_auth import hash_password
from ..util.util import str_to_none

registration: Blueprint = Blueprint("registration", __name__)


def validate_password(password: str) -> None | str:
    """
    Validates a password according to the following rules:
        - Must contain at least 1 lowercase character.
        - Must contain at least 1 uppercase character.
        - Must contain at least 1 digit (0 through 9).

    :param password: Password to validate.
    :return: Error message if password doesn't meet the specified criteria; None otherwise.
    """

    errors: list[str] = []
    error_msg_prefix: str = "Password must contain"
    error_msg: str

    lower: bool = False
    upper: bool = False
    digit: bool = False

    for char in password:
        code: int = ord(char)  # Evaluating unicode codes (see ASCII Table)

        if code in range(48, 58):
            digit = True
        elif code in range(65, 91):
            upper = True
        elif code in range(97, 122):
            lower = True

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

    if "user" in session:
        current_app.logger.info(f"[page='/register'] => Authenticated user tried to access restricted page")
        flash("You must log out before creating a new account", category="error")
        return redirect("/profile")

    # Load insensitive data back into the form after a failed
    # submission so user does not need to re-enter it all.
    username: str = request.args.get("username", None)
    user_type: str = request.args.get("user_type", None)

    first_name: str = request.args.get("first_name", None)
    last_name: str = request.args.get("last_name", None)
    age: str = request.args.get("age", None)
    email: str = request.args.get("email", None)
    phone: str = request.args.get("phone", None)
    gender: str = request.args.get("gender", None)

    return render_template(
        template_name_or_list="html/register.html",
        username=username, user_type=user_type, first_name=first_name,
        last_name=last_name, age=age, email=email, phone=phone, gender=gender
    )


@registration.route("/register", methods=["POST"])
def register_post() -> Response:
    """
    Function called when registration form is submitted.
    """

    # Required inputs
    username: str = str_to_none(request.form["register-username"])
    password: str = str_to_none(request.form["register-password"])
    confirm_password: str = str_to_none(request.form["register-confirm-password"])
    captcha_response: str = str_to_none(request.form["g-recaptcha-response"])
    user_type: str = request.form.get("register-user-type", None)

    # Non required inputs
    first_name: str = str_to_none(request.form["register-first-name"])
    last_name: str = str_to_none(request.form["register-last-name"])
    age: str = str_to_none(request.form["register-age"])
    email: str = str_to_none(request.form["register-email"])
    phone: str = str_to_none(request.form["register-phone"])
    gender: str = request.form.get("register-gender", None)

    page: Response = redirect(
        url_for(endpoint=".register_get", username=username, user_type=user_type,
                first_name=first_name, last_name=last_name, age=age, email=email,
                phone=phone, gender=gender)
    )

    if not captcha_response:
        current_app.logger.warning("[page='/register' (FORM)] => CAPTCHA not completed")
        flash("Please complete the CAPTCHA before form submission", category="error")
        return page

    if user_type is None:
        current_app.logger.warning("[page='/register' (FORM)] => User account type not selected")
        flash("Please select a user type for your account", category="error")
        return page

    if user_exists(username):
        current_app.logger.warning("[page='/register' (FORM)] => Given username is taken")
        flash(f"Sorry, the username {username!r} is taken!", category="error")
        return page

    password_error_msg: None | str = validate_password(password)

    if password_error_msg is not None:
        current_app.logger.warning(f"[page='/register' (FORM)] => {password_error_msg}")
        flash(password_error_msg, category="error")
        return page

    if confirm_password != password:
        current_app.logger.warning(f"[page='/register' (FORM)] => Password mismatch")
        flash("Passwords do not match", category="error")
        return page

    hashed_pw: str = hash_password(password=password)

    current_app.logger.info(f"[page='/register' (FORM)] => Registration ticket opened for user: {username!r}")
    flash(f"Registration ticket opened. Awaiting administrator approval for: {username!r}", category="info")

    create_user(
        username=username, password=hashed_pw, user_type=user_type, first_name=first_name,
        last_name=last_name, age=age, email=email, phone=phone, gender=gender
    )

    return redirect("/home")
