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

import api
import config
import helpers
import utils
from utils import alert, csrf
from utils import image as img
from utils import session as sesh

app = Flask(__name__)
app.secret_key = config.secret_key


# * For testing and debugging
if app.debug:

    @app.route("/session")
    def show_session():
        return list(session.items())


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
    csrf.init()

    posts = api.posts.get_all()
    users = api.users.get_all()
    return render_template("index.html", posts=posts, users=users)


@app.route("/i/<filename>")
def image(filename):
    return send_from_directory(
        os.path.join(app.root_path, "uploads"), filename
    )


@app.route("/post/<post_id>")
def post(post_id):
    post = api.posts.get(post_id)
    post = utils.to_localtime(post)
    return render_template("post.html", post=post)


@app.route("/login")
def login():
    if sesh.validate():
        return redirect("/")

    csrf.init()
    return render_template("login.html")


@app.route("/api/user/login", methods=["POST"])
def login_user():
    username = request.form["username"].strip().lower()
    password = request.form["password"].strip()

    csrf.validate()

    if not helpers.is_username_valid(username):
        alert.set("ERROR: Username is not valid")
        return redirect("/login")

    if not helpers.is_password_valid(password):
        alert.set("ERROR: Password is not valid")
        return redirect("/login")

    result = api.users.get_login(username)

    if not result:
        alert.set(f"ERROR: wrong username or password {result}")
        return redirect("/login")

    user_id, username, display_name, password_hash = result

    if check_password_hash(password_hash, password):
        sesh.set(user_id, username, display_name)
    else:
        alert.set("ERROR: wrong username or password")
        return redirect("/login")

    alert.clear()
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register")
def register():
    if sesh.validate():
        return redirect("/")

    csrf.init()
    return render_template("register.html")


@app.route("/api/user/create", methods=["POST"])
def new_user():
    csrf.validate()

    display_name = request.form["username"].strip()
    username = display_name.lower()
    password = request.form["password"].strip()
    password1 = request.form["password1"].strip()

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


@app.route("/alert/clear", methods=["POST"])
def clear_alert_route():
    csrf.validate()
    alert.clear()
    return redirect(request.referrer)


@app.route("/user")
def user():
    if sesh.validate():
        return redirect("/user/me")
    return redirect("/login")


@app.route("/me")
def me():
    return redirect("/user/me")


@app.route("/user/<user>")
def user_page(user):
    user = user.strip().lower()

    user_posts = []
    if sesh.validate() and (user == "me" or user == session["user_id"]):
        user = session["user_id"]
        user_posts = api.posts.get_unlisted_of(user)
    elif user == "me" and not sesh.validate():
        return redirect("/login")
    else:
        user_posts = api.posts.get_all_of(user)

    posts = [utils.to_localtime(post) for post in user_posts]
    user_data = api.users.get(user)

    return render_template("user.html", user=user_data, posts=posts)


@app.route("/post")
def create_post():
    if not sesh.validate():
        return redirect("/login")

    csrf.init()
    return render_template("create_post.html")


@app.route("/api/post/create", methods=["POST"])
def new_post():
    csrf.validate()
    sesh.require_login()

    title = ""
    if "title" in request.form:
        title = request.form["title"].strip()

    description = ""
    if "description" in request.form:
        description = request.form["description"].strip()

    unlisted = False
    if "unlisted" in request.form:
        unlisted = bool(request.form["unlisted"])

    file = None
    if "file" in request.files:
        file = request.files["file"]

    if not helpers.is_title_valid(title):
        alert.set("ERROR: Title is not valid")
        return redirect("/post")

    if not helpers.is_description_valid(description):
        alert.set("ERROR: Description is not valid")
        return redirect("/post")

    if not file:
        alert.set("ERROR: File not found")
        return redirect("/post")

    if not str(file.filename).endswith((".jpg", ".jpeg")):
        alert.set("ERROR: File extension is not valid, must be (.jpg, .jpeg)")
        return redirect("/post")

    data = file.read()

    max_size_kb = 500
    max_size_bytes = max_size_kb * 1024

    if len(data) > max_size_bytes:
        alert.set(f"ERROR: File size too big (max {max_size_bytes} bytes)")
        return redirect("/post")

    if not img.validate_jpg_signature(data):
        alert.set("ERROR: File is not valid, must be (.jpg, .jpeg)")
        return redirect("/post")

    result = api.posts.create(title, description, unlisted)
    post_id = None if not result and "id" not in result else result["id"]

    if not post_id:
        alert.set("ERROR: Post could not be returned")
        return redirect("/post")

    img.save_jpg(data, post_id)
    api.posts.update_filename(post_id, f"{post_id}.jpg")

    return redirect(f"/post/{post_id}")
