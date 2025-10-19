import sqlite3

from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

import api
import routes.helpers as helpers
from routes.helpers import alert, csrf, to_localtime
from routes.helpers import session as sesh

__all__ = [
    "create",
    "create_view",
    "edit_view",
    "goto_user_edit",
    "login",
    "login_view",
    "logout",
    "me",
    "update",
    "view",
]


def create():
    csrf.validate()

    display_name = request.form.get("username", "", str).strip()
    username = display_name.lower()

    password = request.form.get("password", "", str).strip()
    password1 = request.form.get("password1", "", str).strip()

    if not helpers.is_username_valid(username):
        alert.set("ERROR: username is not valid")
        return redirect("/register")

    if not helpers.is_password_valid(password):
        alert.set("ERROR: password is not valid")
        return redirect("/register")

    if password != password1:
        alert.set("ERROR: passwords are not the same")
        return redirect("/register")

    password_hash = generate_password_hash(password)

    try:
        result = api.users.create(display_name, password_hash)
        if result:
            sesh.set(result["id"], result["username"], result["display_name"])

        alert.clear()

        return redirect("/user/me")
    except sqlite3.IntegrityError:
        alert.set("ERROR: username already taken")
        return redirect("/register")


def create_view():
    if sesh.has_session():
        return redirect("/")

    csrf.init()
    return render_template("user_form.html")


def edit_view():
    if not sesh.has_session():
        return redirect("/login")

    user = api.users.get(session.get("user_id", None))

    if not user:
        return redirect("/")

    if not sesh.is_user(user):
        return redirect("/user/me")

    csrf.init()
    return render_template("edit_user_form.html", user=user)


def goto_user_edit():
    if sesh.has_session():
        return redirect("/user/me/edit")
    return redirect("/login")


def login():
    username = request.form.get("username", "", str).strip().lower()
    password = request.form.get("password", "", str).strip()

    csrf.validate()

    if not username or not helpers.is_username_valid(username):
        alert.set("ERROR: username is not valid")
        return redirect("/login")

    if not password or not helpers.is_password_valid(password):
        alert.set("ERROR: password is not valid")
        return redirect("/login")

    result = api.users.get_login(username)

    if not result:
        alert.set("ERROR: wrong username or password")
        return redirect("/login")

    user_id, username, display_name, password_hash = result

    if check_password_hash(password_hash, password):
        sesh.set(user_id, username, display_name)
    else:
        alert.set("ERROR: wrong username or password")
        return redirect("/login")

    alert.clear()
    return redirect("/")


def login_view():
    if sesh.has_session():
        return redirect("/")

    csrf.init()
    return render_template("login_form.html")


def logout():
    session.clear()
    return redirect("/")


def me():
    if sesh.has_session():
        return redirect("/user/me")
    return redirect("/login")


def update():
    sesh.require_session()
    csrf.validate()

    if "cancel" in request.form:
        return redirect("/user/me")

    result = api.users.get_login(session.get("user_id", None))
    sesh.authenticate(result)

    user_id, username, display_name, password_hash = result

    new_display_name = request.form.get("display_name", "", str).strip()

    if not new_display_name:
        new_display_name = display_name

    password = request.form.get("password", "", str).strip()
    new_password = request.form.get("new_password", "", str).strip()
    new_password1 = request.form.get("new_password1", "", str).strip()

    new_password_hash = password_hash

    display_name_changed = display_name != new_display_name
    password_changed = password and new_password and new_password1

    errors = set()
    is_valid = True
    if display_name_changed and new_display_name.lower() != username:
        errors.add(
            "display name is not valid (can only change capitalization)"
        )
        is_valid = False

    if not is_valid:
        return helpers.redirect_with_errors("/user/me/edit", errors)

    if password_changed:
        if not helpers.is_password_valid(password):
            errors.add("old password is not valid")
            is_valid = False

        if not helpers.is_password_valid(new_password):
            errors.add("new password is not valid")
            is_valid = False

        if new_password != new_password1:
            errors.add("new passwords are not the same")
            is_valid = False

        if not check_password_hash(password_hash, password):
            errors.add("old password is not valid")
            is_valid = False

        if check_password_hash(password_hash, new_password):
            errors.add("old and new passwords are the same")
            is_valid = False

        if not is_valid:
            return helpers.redirect_with_errors("/user/me/edit", errors)

        new_password_hash = generate_password_hash(new_password)

    message = "User was not edited"
    if display_name_changed or password_changed:
        result = api.users.update(user_id, new_display_name, new_password_hash)
        sesh.set(result["id"], result["username"], result["display_name"])

        message = "Display name and password changed"
        if display_name_changed and not password_changed:
            message = "Display name changed"
        elif not display_name_changed and password_changed:
            message = "Password changed"

    alert.set(message)
    return redirect("/user/me")


def view(user):
    user_posts = []
    if sesh.has_session() and user in ("me", session["user_id"]):
        user = session["user_id"]
        user_posts = api.posts.get_unlisted_of(user)
    elif user == "me" and not sesh.has_session():
        return redirect("/login")
    else:
        user_posts = api.posts.get_all_of(user)

    posts = [to_localtime(post) for post in user_posts]
    user_data = api.users.get(user)

    return render_template("user.html", user=user_data, posts=posts)
