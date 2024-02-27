from werkzeug.datastructures.structures import ImmutableMultiDict
from colorama import Fore


def get_boolean_input(prompt: str) -> bool:

    while True:
        _input: str = input(prompt).lower().replace(" ", "")

        if _input in ("yes", "y"):
            return True

        if _input in ("no", "n"):
            return False

        print(f"{Fore.LIGHTRED_EX}Please enter 'yes' or 'no'{Fore.RESET}")


def str_to_none(string: str) -> str | None:
    """
    Maps a string to None if it is an empty string.

    :param string: String to evaluate.
    """

    return None if not string or string is None else string


def get_form_user_details(form_data: ImmutableMultiDict[str, str]) -> tuple[str | None, ...]:
    return (
        str_to_none(form_data["first-name-input"]),
        str_to_none(form_data["last-name-input"]),
        str_to_none(form_data["age-input"]),
        str_to_none(form_data["email-input"]),
        str_to_none(form_data["phone-input"]),
        form_data.get("gender-input", None)
    )
