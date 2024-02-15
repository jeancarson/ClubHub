from flask import Blueprint, render_template

misc: Blueprint = Blueprint("misc", __name__)


@misc.route("/about")
@misc.route("/about-us")
def about_us() -> str:
    """
    Loads the about page.
    """

    return render_template("html/misc/about.html")


@misc.route("/contact")
@misc.route("/contact-us")
def contact() -> str:
    """
    Loads the contact page.
    """

    return render_template("html/misc/contact.html")


@misc.route("/privacy-policy")
def privacy_policy() -> str:
    """
    Loads the privacy policy page.
    """

    return render_template("html/misc/privacy-policy.html")


@misc.route("/terms-and-conditions")
def terms_and_conditions() -> str:
    """
    Loads the terms and conditions page.
    """

    return render_template("html/misc/terms-and-conditions.html")


@misc.route("/forgot-password")
def forgot_password() -> str:
    """
    Loads the forgot password page.
    """

    return render_template("html/auth/forgot-password.html")
