from flask import (
    Blueprint,
    Response,
    request,
    redirect,
    render_template
)

from ..util.authentication import current_user, current_user_info
from ..util.authentication.alerts import error, success, Error, Success

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

    return render_template("html/misc/profile.html", user_info=current_user_info())


@profile.route("/edit")
def profile_edit() -> str | Response:
    """
    Loads the profile page with a form (if a user session is active).
    """

    user: str | None = current_user()

    if user is None:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint="/profile")
        return redirect("/home")

    return render_template("html/misc/profile.html", user_info=current_user_info(), edit=True)


@profile.route("/profile", methods=["POST"])
def profile_post() -> Response:
    """
    Loaded when profile is saved.
    """

    # TODO: Get and save profile info

    return redirect("/profile")
