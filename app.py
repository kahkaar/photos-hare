import os
import sqlite3

from flask import (
    Flask,
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
    if session.keys():
        return redirect("/")
    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]

    user_id, password_hash = db.query(queries.get_user, [username])

    if password_hash and check_password_hash(password_hash[0][0], password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "ERROR: wrong username or password"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register")
def register():
    if session.keys():
        return redirect("/")
    return render_template("register.html")


@app.route("/api/new_user", methods=["POST"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    password1 = request.form["password1"]

    if password != password1:
        return "ERROR: passwords are not the same"

    password_hash = generate_password_hash(password)

    try:
        db.execute(queries.create_user, [username, password_hash])
        user_id = db.query(queries.get_user_id, [username])[0][0]
        session["username"] = username
        session["user_id"] = user_id
    except sqlite3.IntegrityError:
        return "ERROR: username already taken"

    return redirect("/")
