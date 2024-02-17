from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flask import current_app, flash


@dataclass(kw_only=True)
class Alert:
    log: str
    message: str


class Error(Enum):
    RESTRICTED_PAGE_LOGGED_OUT = Alert(
        log="Unauthenticated user tried to access restricted page",
        message="You cannot access this page as you are not logged in"
    )

    RESTRICTED_PAGE_LOGGED_IN = Alert(
        log="Authenticated user tried to access restricted page",
        message="You are already logged in as {user}"
    )

    RESTRICTED_PAGE_ADMIN = Alert(
        log="{user_type} tried to access Administrator-only page",
        message="Only Administrators can access that page!"
    )

    NO_CAPTCHA = Alert(
        log="CAPTCHA not completed",
        message="Please complete the CAPTCHA before form submission"
    )

    NO_USER_TYPE = Alert(
        log="User account type not selected",
        message="Please select a user type for your account"
    )

    USERNAME_TAKEN = Alert(
        log="Given username is taken",
        message="Sorry, the username {username} is taken!"
    )

    INVALID_PW = Alert(
        log="{err}",
        message="{err}"
    )

    PW_MISMATCH = Alert(
        log="Password mismatch",
        message="Passwords do not match"
    )

    NO_CLUB_NAME = Alert(
        log="No club name given for user of type COORDINATOR",
        message="Please provide a club name"
    )

    UNAPPROVED = Alert(
        log="Account {username!r} still awaiting administrator approval",
        message="Your account, {username}, is awaiting administrator approval"
    )

    INCORRECT_PW = Alert(
        log="Incorrect password for {username!r}",
        message="Incorrect password"
    )

    INVALID_USERNAME = Alert(
        log="Invalid username: {username!r}",
        message="User not found: {username}"
    )


class Success(Enum):
    LOGIN = Alert(
        log="Login successful for user: {username!r} <{user_type}>",
        message="Successfully logged in: {username}"
    )

    LOGOUT = Alert(
        log="Logout successful for user: {user!r}",
        message="You have been logged out. See you later {user}!"
    )

    REGISTER = Alert(
        log="Registration ticket opened for user: {username!r}",
        message="Registration ticket opened. Awaiting administrator approval for: {username}"
    )

    REGISTER_ADMIN = Alert(
        log="Administrator registration successful: {username!r}",
        message="You are now logged in, {username}!"
    )


def _alert(*, alert_type: Error | Success, endpoint: str, category: str, form: Optional[bool] = None, **kwargs) -> None:
    form_str: str = " (FORM)" if form else ""

    current_app.logger.info(f"[endpoint={endpoint!r}{form_str}] => {alert_type.value.log.format(**kwargs)}")
    flash(alert_type.value.message.format(**kwargs), category=category)


def error(*, errtype: Error, endpoint: str, form: Optional[bool] = None, **kwargs) -> None:
    _alert(
        alert_type=errtype,
        endpoint=endpoint,
        category="error",
        form=form,
        **kwargs
    )


def success(*, successtype: Success, endpoint: str, form: Optional[bool] = None, **kwargs) -> None:
    _alert(
        alert_type=successtype,
        endpoint=endpoint,
        category="info",
        form=form,
        **kwargs
    )
