from flask import abort, session


def set(id, username, display_name):
    username = username.strip().lower()
    display_name = display_name.strip() if display_name else username
    session["user_id"] = id
    session["username"] = username
    session["display_name"] = display_name


def validate():
    session_keys = ["user_id", "username", "display_name"]
    for key in session_keys:
        if key not in list(session.keys()):
            return False
    return True


def require_login():
    if not validate():
        abort(403)
