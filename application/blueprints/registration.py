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

registration: Blueprint = Blueprint("registration", __name__)


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
    form_user_type: str = request.args.get("user_type", "")

    form_first_name: str = request.args.get("first_name", "")
    form_last_name: str = request.args.get("last_name", "")
    form_email: str = request.args.get("email", "")
    form_phone: str = request.args.get("phone", "")
    form_gender: str = request.args.get("gender", "")

    if "user" in session:
        flash("You must log out before creating a new account", category="error")
        return redirect("/profile")

    return render_template(
        template_name_or_list="html/register.html",
        form_username_value=form_username,
        form_user_type_value=form_user_type,
        form_first_name_value=form_first_name,
        form_last_name_value=form_last_name,
        form_email_value=form_email,
        form_phone_value=form_phone,
        form_gender_value=form_gender
    )


@registration.route("/register", methods=["POST"])
def register_post() -> Response:

    print(request.form)

    # Required inputs
    username: str = request.form["register-username"]
    password: str = request.form["register-password"]
    confirm_password: str = request.form["register-confirm-password"]
    captcha_response: str = request.form["g-recaptcha-response"]
    user_type: str = request.form["register-user-type"]

    # Non required inputs
    first_name: str = request.form["register-first-name"]
    last_name: str = request.form["register-first-name"]
    email: str = request.form["register-email"]
    phone: str = request.form["register-phone"]
    gender: str = request.form["register-gender"]

    # TODO: Check if username in registered users already

    page: Response = redirect(
        url_for(
            endpoint=".register_get",
            username=username,
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender
        )
    )

    if not captcha_response:
        flash("Please complete the CAPTCHA before form submission", category="error")
        return page

    if not user_type:
        flash("Please select a user type for your account")
        return page

    password_error_msg: None | str = validate_password(password)

    if password_error_msg:
        flash(password_error_msg, category="error")
        return page

    if confirm_password != password:
        flash("Passwords do not match", category="error")
        return page

    flash(f"Registration ticket opened. Awaiting administrator approval for: {username!r}", category="info")
    return redirect("/home")


@registration.route("/privacy-policy")
def privacy_policy() -> str:
    return render_template("html/privacy-policy.html")
