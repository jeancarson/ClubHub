from flask import (
    Blueprint,
    Response,
    request,
    redirect,
    session,
    render_template
)

from ..util.authentication import current_user, current_user_profile_info
from ..util.authentication.alerts import error, Error
from ..util.db_functions.users import update_user_profile_info
from ..util import get_form_user_details

profile: Blueprint = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/")
def profile_get() -> str | Response:
    """
    Loads the profile page (if a user session is active).
    """

    user: str | None = current_user()

    if user is None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint="/profile")
        return redirect("/home")

    return render_template("html/user/profile.html", user_info=current_user_profile_info())


@profile.route("/edit")
def profile_edit() -> str | Response:
    """
    Loads the profile page with a form (if a user session is active).
    """

    user: str | None = current_user()

    if user is None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint="/profile")
        return redirect("/home")

    return render_template("html/user/profile.html", user_info=current_user_profile_info(), edit=True)


@profile.route("/", methods=["POST"])
def profile_post() -> Response:
    """
    Loaded when profile is saved.
    """

    user_id = session["user-id"]

    # Updated values
    first_name, last_name, age, email, phone, gender = get_form_user_details(form_data=request.form)

    update_user_profile_info(
        user_id=user_id, first_name=first_name, last_name=last_name,
        age=age, email=email, phone=phone, gender=gender
    )

    return redirect("/profile")
