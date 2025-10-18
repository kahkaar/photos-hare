import secrets

from flask import abort, request, session

__all__ = [
    "init",
    "is_valid",
    "validate",
]


def init():
    session["csrf_token"] = secrets.token_hex(16)


def is_valid():
    return request.form.get("csrf_token") == session.get("csrf_token", -1)


def validate():
    if not is_valid():
        abort(403)
