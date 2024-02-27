from flask import Blueprint, render_template

from ..util.authentication import current_user

main: Blueprint = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
@main.route("/home")
def home() -> str:
    """
    Loads the home (default) page.
    """

    user: str | None = current_user()

    if user is not None:
        # Get user type here (stored in session variable) and
        # redirect to coordinator or member home page

        return render_template("html/user/home.html", header=f"Hello {user}!")

    return render_template("html/misc/home.html")
