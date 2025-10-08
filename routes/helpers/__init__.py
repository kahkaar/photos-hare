import os
from datetime import datetime
from re import match

from flask import redirect, request

from . import alert, csrf, jpeg

__all__ = [
    "alert",
    "csrf",
    "jpeg",
    "delete_image",
    "get_referrer",
    "is_comment_valid",
    "is_description_valid",
    "is_password_valid",
    "is_title_valid",
    "is_username_valid",
    "redirect_with_errors",
    "to_localtime",
]


def delete_image(filename):
    dir_path = os.path.join("uploads")
    file_path = os.path.join(dir_path, filename)

    os.makedirs(dir_path, exist_ok=True)

    if os.path.exists(file_path):
        os.remove(file_path)


def get_referrer():
    return request.args.get("ref", "index", str)


def is_comment_valid(comment):
    return 0 <= len(comment) <= 255


def is_description_valid(desc):
    return 0 <= len(desc) <= 255


def is_password_valid(password):
    # * Allowed characters `a-zA-Z0-9_!#$%&()*+-.?` (length 8 to 255 characters)
    pattern = r"^[\w\x21\x23-\x26\x28-\x2e\x3f\x40]{8,255}+$"
    return bool(match(pattern, password))


def is_title_valid(title):
    return 1 <= len(title) <= 255


def is_username_valid(username):
    # * Allowed characters `a-zA-Z0-9_` (length 4 to 24 characters)
    pattern = r"^[\w]{4,24}+$"
    return bool(match(pattern, username))


def redirect_with_errors(location, errors):
    alert.set(f"ERROR: {', '.join(errors)}")
    return redirect(location)


def to_localtime(obj):
    if not obj:
        return obj

    def from_timestamp(ts):
        if not ts:
            return None

        return str(datetime.fromtimestamp(ts).astimezone()).split(
            "+", maxsplit=1
        )[0]

    return {
        **obj,
        "created_at": from_timestamp(obj["created_at"]),
        "updated_at": from_timestamp(obj["updated_at"]),
    }
