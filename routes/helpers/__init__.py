import os
from datetime import datetime
from re import match

from flask import request

from . import alert, csrf, jpeg

__all__ = [
    "alert",
    "csrf",
    "jpeg",
    "delete_image",
    "get_referrer",
    "is_description_valid",
    "is_password_valid",
    "is_title_valid",
    "is_username_valid",
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


def is_description_valid(input):
    return 0 <= len(input) <= 255


def is_password_valid(password):
    # * Allowed characters `a-zA-Z0-9_!#$%&()*+-.?` (length 8 to 255 characters)
    pattern = r"^[\w\x21\x23-\x26\x28-\x2e\x3f\x40]{8,255}+$"
    return bool(match(pattern, password))


def is_title_valid(input):
    return 1 <= len(input) <= 255


def is_username_valid(username):
    # * Allowed characters `a-zA-Z0-9_` (length 4 to 24 characters)
    pattern = r"^[\w]{4,24}+$"
    return bool(match(pattern, username))


def to_localtime(obj):
    if not obj:
        return obj

    def from_timestamp(ts):
        if not ts:
            return None

        return str(datetime.fromtimestamp(ts).astimezone()).split("+")[0]

    return {
        **obj,
        "created_at": from_timestamp(obj["created_at"]),
        "updated_at": from_timestamp(obj["updated_at"]),
    }
