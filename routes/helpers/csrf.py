import secrets

from flask import abort, request, session

__all__ = [
    "init",
    "validate",
]


def init():
    session["csrf_token"] = secrets.token_hex(16)


def validate():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
