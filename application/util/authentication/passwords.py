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
##NOTE for demo purposes can be commented out and the below run
    # return password == hashed
