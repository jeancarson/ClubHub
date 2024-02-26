"""
Validate page access permissions.

Here's an example use case:

    from application.util.authentication.page_access import validate_student_perms

    @app.route("/student-only-page")
    def go_to_student_only_page():

        invalid = validate_student_perms(endpoint="/student-only-page")

        if invalid:
            return invalid

        return render_template("html/student/student-only-page.html")

In this example, the user's access is validated using the validate_student_perms function.

The return value of this function is either the template for the default home page (which is a string),
or None. This return value is stored in a variable, invalid.

In the case that the return value is the template (which is a truthy value),
the conditional evaluation of the variable, invalid, results in True, so the function
will return that value instead of proceeding.

Otherwise, if the return value is None, then the evaluation will result in False,
and the function will continue until returning the requested page.
"""

from functools import partial
from typing import Callable

from flask import session, render_template

from .alerts import error, Error


def validate_access_perms(user_type: str, endpoint: str) -> str | None:
    """
    Returns the default home page if no user is currently logged in,
    or if they do not have privileges to access a given page. Returns None otherwise.

    :param user_type: User type required to access the given endpoint:
                      One of "ADMINISTRATOR", "STUDENT" or "COORDINATOR".
    :param endpoint: Endpoint of url user wants to access.
    """

    if "user" not in session:
        error(errtype=Error.RESTRICTED_PAGE_LOGGED_OUT, endpoint=endpoint)
        return render_template("html/misc/home.html")

    current_user_type: str = session["user-type"]

    if current_user_type != user_type:
        errtype: Error = Error[f"RESTRICTED_PAGE_{user_type}"]
        error(errtype=errtype, endpoint=endpoint, user_type=current_user_type)
        return render_template("html/misc/home.html")

    return None


# Alias functions with default arguments
validate_student_perms: Callable = partial(validate_access_perms, user_type="STUDENT")
validate_coordinator_perms: Callable = partial(validate_access_perms, user_type="COORDINATOR")
validate_admin_perms: Callable = partial(validate_access_perms, user_type="ADMINISTRATOR")
