
def str_to_none(string: str) -> str | None:
    """
    Maps a string to None if it is an empty string.

    :param string: String to evaluate.
    """

    return None if not string or string is None else string
