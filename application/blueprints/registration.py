from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for
)
from werkzeug import Response

from ..util.authentication import current_user, login
from ..util.authentication.alerts import error, success, Error, Success
from ..util.authentication.passwords import hash_password
from ..util.db_functions.users import user_exists, create_user
from ..util import str_to_none, get_form_user_details

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

    user: str | None = current_user()

    if user is not None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_IN, endpoint="/register", user=user)
        return redirect("/profile")

    # Load insensitive data back into the form after a failed
    # submission so user does not need to re-enter it all.
    username: str = request.args.get("username", None)
    user_type: str = request.args.get("user_type", None)
    club_name: str = request.args.get("club_name", None)
    club_description: str = request.args.get("club_description")
    first_name: str = request.args.get("first_name", None)
    last_name: str = request.args.get("last_name", None)
    age: str = request.args.get("age", None)
    email: str = request.args.get("email", None)
    phone: str = request.args.get("phone", None)
    gender: str = request.args.get("gender", None)

    return render_template(
        template_name_or_list="html/auth/register.html",
        username=username, user_type=user_type, club_name=club_name, club_description=club_description,
        first_name=first_name, last_name=last_name, age=age, email=email, phone=phone, gender=gender
    )


@registration.route("/register", methods=["POST"])
def register_post() -> Response:
    """
    Function called when registration form is submitted.
    """

    print(request.form)

    # Required inputs
    username: str | None = str_to_none(request.form["register-username"])
    password: str | None = str_to_none(request.form["register-password"])
    confirm_password: str | None = str_to_none(request.form["register-confirm-password"])
    captcha_response: str | None = str_to_none(request.form["g-recaptcha-response"])
    user_type: str | None = request.form.get("register-user-type", None)
    club_name: str | None = str_to_none(request.form["register-club-name"])

    # Non-required inputs
    club_description: str | None = str_to_none(request.form["register-club-description"])
    first_name, last_name, age, email, phone, gender = get_form_user_details(form_data=request.form)

    page: Response = redirect(
        url_for(endpoint=".register_get", username=username, user_type=user_type,
                club_name=club_name, club_description=club_description, first_name=first_name,
                last_name=last_name, age=age, email=email, phone=phone, gender=gender)
    )

    if not captcha_response:
        error(errtype=Error.NO_CAPTCHA, endpoint="/register", form=True)
        return page

    if user_type is None:
        error(errtype=Error.NO_USER_TYPE, endpoint="/register", form=True)
        return page

    elif user_type == "COORDINATOR" and club_name is None:
        error(errtype=Error.NO_CLUB_NAME, endpoint="/register", form=True)
        return page

    if user_exists(username):
        error(errtype=Error.USERNAME_TAKEN, endpoint="/register", form=True, username=username)
        return page

    password_error_msg: None | str = validate_password(password)

    if password_error_msg is not None:
        error(errtype=Error.INVALID_PW, endpoint="/register", form=True, err=password_error_msg)
        return page

    if confirm_password != password:
        error(errtype=Error.PW_MISMATCH, endpoint="/register", form=True)
        return page

    hashed_pw: str = hash_password(password=password)

    first_user: bool = create_user(
        username=username, password=hashed_pw, user_type=user_type, first_name=first_name,
        last_name=last_name, age=age, email=email, phone=phone, gender=gender, club_name=club_name,
        club_description=club_description
    )

    if first_user:
        login(user_id=1, username=username, user_type="ADMINISTRATOR")
        success(successtype=Success.REGISTER_ADMIN, endpoint="/register", form=True, username=username)
    else:
        success(successtype=Success.REGISTER, endpoint="/register", form=True, username=username)

    return redirect("/home")
