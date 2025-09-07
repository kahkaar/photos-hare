import os
import re
import secrets
import sqlite3

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
from werkzeug.security import check_password_hash, generate_password_hash

import config
import db
import queries

app = Flask(__name__)
app.secret_key = config.secret_key


# * For testing and debugging
if app.debug:

    @app.route("/session")
    def show_session():
        return list(session.items())


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


def set_session(id, username, display_name):
    username = username.strip().lower()
    display_name = display_name.strip() if display_name else username
    session["user_id"] = id
    session["username"] = username
    session["display_name"] = display_name


def check_session():
    session_keys = ["user_id", "username", "display_name"]
    for key in session_keys:
        if key not in list(session.keys()):
            return False
    return True


def require_login():
    if check_session():
        abort(403)


def is_username_valid(username):
    # * Allowed characters `a-zA-Z0-9_` (length 4 to 24 characters)
    pattern = r"^[\w]{4,24}+$"
    return bool(re.match(pattern, username))


def is_password_valid(password):
    # * Allowed characters `a-zA-Z0-9_!#$%&()*+-.?` (length 8 to 255 characters)
    pattern = r"^[\w\x21\x23-\x26\x28-\x2e\x3f\x40]{8,255}+$"
    return bool(re.match(pattern, password))


# TODO: Add favicon.ico (and favicon.svg)
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static", "images"),
        "favicon.ico",
        mimetype="image/x-icon",
    )


@app.route("/")
def index():
    posts = db.query(queries.get_posts)
    users = db.query(queries.get_users)
    return render_template("index.html", posts=posts, users=users)


@app.route("/login")
def login():
    if check_session():
        return redirect("/")

    session["csrf_token"] = secrets.token_hex(16)
    return render_template("login.html")


@app.route("/api/user/login", methods=["POST"])
def login_user():
    username = request.form["username"].strip().lower()
    password = request.form["password"].strip()

    check_csrf()

    if not is_username_valid(username):
        return "ERROR: username is not valid"

    if not is_password_valid(password):
        return "ERROR: password is not valid"

    result = db.query(queries.get_user, [username])
    if not list(result):
        return "ERROR: wrong username or password"

    user_id, username, display_name, password_hash = result[0]

    if check_password_hash(password_hash, password):
        set_session(user_id, username, display_name)
    else:
        return "ERROR: wrong username or password"

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register")
def register():
    if check_session():
        return redirect("/")

    session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")


@app.route("/api/user/create", methods=["POST"])
def new_user():
    display_name = request.form["username"].strip()
    username = display_name.lower()
    password = request.form["password"].strip()
    password1 = request.form["password1"].strip()

    check_csrf()

    if not is_username_valid(username):
        return "ERROR: username is not valid"

    if not is_password_valid(password):
        return "ERROR: password is not valid"

    if password != password1:
        return "ERROR: passwords are not the same"

    password_hash = generate_password_hash(password)

    try:
        db.execute(
            queries.create_user, [username, display_name, password_hash]
        )
        user_id = db.query(queries.get_user_id, [username])[0]["id"]
        set_session(user_id, username, display_name)

        # TODO: Redirect to 'account' page
        del session["csrf_token"]
        return redirect("/login")
    except sqlite3.IntegrityError:
        return "ERROR: username already taken"
