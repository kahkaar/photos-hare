import secrets

from flask import abort, request, session

__all__ = [
    "init",
    "validate",
]


def init():
    session["csrf_token"] = secrets.token_hex(16)


def validate():
    if request.form.get("csrf_token") != session.get("csrf_token", -1):
        abort(403)
