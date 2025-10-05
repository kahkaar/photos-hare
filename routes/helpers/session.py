from flask import abort, session

__all__ = [
    "authenticate",
    "is_owner",
    "is_user",
    "require_login",
    "require_ownership",
    "set",
    "validate",
]


SESSION_KEYS = {"display_name", "user_id", "username"}


def authenticate(user):
    if not is_user(user):
        abort(403)


def is_owner(post):
    return session["user_id"] == post["user_id"]


def is_user(user):
    return session["user_id"] == user["id"]


def require_login():
    if not validate():
        abort(403)


def require_ownership(post):
    if not is_owner(post):
        abort(403)


def set(user_id, username, display_name):
    session["user_id"] = user_id
    session["username"] = username
    session["display_name"] = display_name


def validate():
    current_keys = list(session.keys())
    for key in SESSION_KEYS:
        if key not in current_keys:
            return False
    return True
