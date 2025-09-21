from re import match

__all__ = [
    "is_description_valid",
    "is_password_valid",
    "is_title_valid",
    "is_username_valid",
]


def is_username_valid(username):
    # * Allowed characters `a-zA-Z0-9_` (length 4 to 24 characters)
    pattern = r"^[\w]{4,24}+$"
    return bool(match(pattern, username))


def is_password_valid(password):
    # * Allowed characters `a-zA-Z0-9_!#$%&()*+-.?` (length 8 to 255 characters)
    pattern = r"^[\w\x21\x23-\x26\x28-\x2e\x3f\x40]{8,255}+$"
    return bool(match(pattern, password))


def is_title_valid(input):
    return 1 <= len(input) <= 255


def is_description_valid(input):
    return 0 <= len(input) <= 255
