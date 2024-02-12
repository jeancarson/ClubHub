from flask import Blueprint, session, render_template

main: Blueprint = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
@main.route("/home")
def home() -> str:
    """
    Loads the home (default) page.
    """

    if "user" in session:
        user: str = session["user"]

        # Get user type here (we could store it in the session variable) and
        # redirect to coordinator or member home page

        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/index.html")
