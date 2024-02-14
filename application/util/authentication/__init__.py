from enum import Enum
from flask import session


def current_user() -> str | None:
    return session.get("user", None)


def login(username: str, user_type: str) -> None:
    session["user"] = username
    session["user-type"] = user_type


def logout() -> None:
    del session["user"]
    del session["user-type"]
