from bcrypt import hashpw, checkpw, gensalt


def hash_password(password: str) -> str:
    """
    Hashes the password using the bcrypt password-hashing function,
    which incorporates a randomly generated salt.

    :param password: Password to hash (in plain text).
    :return: Hashed password (with salt integrated) as a hexadecimal string.
    """

    pw_bytes: bytes = password.encode(encoding="utf-8")
    pw_salt: bytes = gensalt()

    return hashpw(password=pw_bytes, salt=pw_salt).hex()


def password_match(password: str, hashed: str) -> bool:
    """
    Compares a password with a corresponding hashed password.

    :param password: Password to check (in plain text).
    :param hashed: Hashed password to compare password against.
    :return: True if password matches the hash; False otherwise.
    """

    pw_bytes: bytes = password.encode(encoding="utf-8")
    hashed_bytes: bytes = bytes.fromhex(hashed)

    return checkpw(password=pw_bytes, hashed_password=hashed_bytes)


def validate_password(password: str) -> None | str:
    """
    Validates a password according to the following rules:
        - Must contain at least 1 lowercase character.
        - Must contain at least 1 uppercase character.
        - Must contain at least 1 digit (0 through 9).

    :param password: Password to validate.
    :return: Error message if password doesn't meet the specified criteria; None otherwise.
    """

    errors: list[str] = []
    error_msg_prefix: str = "Password must contain"
    error_msg: str

    lower: bool = False
    upper: bool = False
    digit: bool = False

    for char in password:
        code: int = ord(char)  # Evaluating unicode codes (see ASCII Table)

        if code in range(48, 58):
            digit = True
        elif code in range(65, 91):
            upper = True
        elif code in range(97, 122):
            lower = True

    if not upper:
        errors.append("a lowercase character")
    if not lower:
        errors.append("an uppercase character")
    if not digit:
        errors.append("a digit")

    if not errors:
        return None

    if len(errors) == 1:
        error_msg = errors[0]
    elif len(errors) == 2:
        error_msg_prefix += ":"
        error_msg = f"{errors[0]} and {errors[1]}"
    else:
        error_msg_prefix += ":"
        error_msg = f"{errors[0]}, {errors[1]}, and {errors[2]}"

    return f"{error_msg_prefix} {error_msg}"
