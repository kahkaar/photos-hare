from flask import abort, session

__all__ = [
    "authenticate",
    "has_session",
    "is_owner",
    "is_user",
    "require_ownership",
    "require_session",
    "set",
]


SESSION_KEYS = {"display_name", "user_id", "username"}


def authenticate(user):
    if not is_user(user):
        abort(403)


def has_session():
    current_keys = list(session.keys())
    for key in SESSION_KEYS:
        if key not in current_keys:
            return False
    return True


def is_owner(post):
    return dict(post).get("user_id") == session.get("user_id", -1)


def is_user(user):
    return dict(user).get("id") == session.get("user_id", -1)


def require_ownership(post):
    if not is_owner(post):
        abort(403)


def require_session():
    if not has_session():
        abort(403)


def set(user_id, username, display_name):
    session["user_id"] = user_id
    session["username"] = username
    session["display_name"] = display_name
