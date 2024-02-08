from flask import Blueprint, render_template


misc: Blueprint = Blueprint("misc", __name__)


@misc.route("/about")
@misc.route("/about-us")
def about_us() -> str:
    """
    Loads the about page.
    """

    return render_template("html/about.html")

