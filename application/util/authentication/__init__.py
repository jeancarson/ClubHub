from flask import session
from sqlite3 import Row

from ..db_functions import get_user_info


def current_user() -> str | None:
    return session.get("user", None)


def current_user_info() -> Row:
    return get_user_info(session["user-id"])


def login(user_id: int, username: str, user_type: str) -> None:
    session["user-id"] = user_id
    session["user"] = username
    session["user-type"] = user_type


def logout() -> None:
    del session["user"]
    del session["user-type"]
