from enum import Enum
from flask import session


class UserType(Enum):
    STUDENT = "STUDENT"
    COORDINATOR = "COORDINATOR"
    ADMINISTRATOR = "ADMINISTRATOR"


def current_user() -> str | None:
    return session.get("user", None)


def login(username: str, user_type: str) -> None:
    session["user"] = username
    session["user-type"] = UserType(user_type)


def logout() -> None:
    del session["user"]
    del session["user-type"]
