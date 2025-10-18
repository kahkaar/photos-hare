from flask import Flask, abort, redirect, request, session

import config
import routes

app = Flask(__name__)
app.secret_key = config.secret_key


# * For testing and debugging
if app.debug:

    @app.route("/session")
    def show_session():
        return list(session.items())


@app.errorhandler(403)
def forbidden(e):
    return routes.error.forbidden(e)


@app.errorhandler(404)
def not_found(e):
    return routes.error.not_found(e)


@app.errorhandler(405)
def method_not_allowed(e):
    return routes.error.method_not_allowed()


if not app.debug:

    @app.errorhandler(Exception)
    def fallback_error(e):
        return routes.error.fallback(e)


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return routes.index.view()
    abort(405)


@app.route("/favicon.<ext>", methods=["GET"])
def favicon(ext):
    if request.method == "GET":
        return routes.static.favicon(ext)
    abort(405)


@app.route("/style.css", methods=["GET"])
def style():
    if request.method == "GET":
        return routes.static.style()
    abort(405)


@app.route("/alert/clear", methods=["POST"])
def clear_alert():
    if request.method == "POST":
        return routes.alert.clear()
    abort(405)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return routes.user.create_view()

    if request.method == "POST":
        return routes.user.create()

    abort(405)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return routes.user.login_view()

    if request.method == "POST":
        return routes.user.login()

    abort(405)


@app.route("/logout", methods=["GET"])
def logout():
    if request.method == "GET":
        return routes.user.logout()

    abort(405)


@app.route("/user/me/edit", methods=["GET", "POST"])
def edit_user():
    if request.method == "GET":
        return routes.user.edit_view()

    if request.method == "POST":
        return routes.user.update()

    abort(405)


@app.route("/me", methods=["GET"])
@app.route("/user/", methods=["GET"])
def me():
    if request.method == "GET":
        return routes.user.me()
    abort(405)


@app.route("/user/<user>", methods=["GET", "POST"])
def user_view(user):
    user = user.strip().lower()

    if request.method == "GET":
        return routes.user.view(user)

    if request.method == "POST":
        return routes.user.goto_user_edit()

    abort(405)


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return routes.post.create_view()

    if request.method == "POST":
        return routes.post.create()

    abort(405)


@app.route("/post/", methods=["GET"])
def post_view_redirect():
    if request.method == "GET":
        return redirect("/post/notfound")
    abort(405)


@app.route("/post/<post_id>/", methods=["GET"])
def post_view_id_redirect(post_id):
    post_id = post_id.strip().lower()

    if request.method == "GET":
        return redirect(f"/post/{post_id}")
    abort(405)


@app.route("/post/<post_id>", methods=["GET"])
def post_view(post_id):
    post_id = post_id.strip().lower()

    if request.method == "GET":
        return routes.post.view(post_id)
    abort(405)


@app.route("/post/<post_id>/comment", methods=["POST"])
def comment_post(post_id):
    post_id = post_id.strip().lower()

    if request.method == "POST":
        return routes.post.comment(post_id)
    abort(405)


@app.route("/post/<post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post_id = post_id.strip().lower()

    if request.method == "GET":
        return routes.post.delete_view(post_id)

    if request.method == "POST":
        return routes.post.delete(post_id)

    abort(405)


@app.route("/post/<post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post_id = post_id.strip().lower()

    if request.method == "GET":
        return routes.post.edit_view(post_id)

    if request.method == "POST":
        return routes.post.update(post_id)

    abort(405)


@app.route("/i/", methods=["GET"])
def image_redirect():
    if request.method == "GET":
        return redirect("/i/notfound")
    abort(405)


@app.route("/i/<filename>", methods=["GET"])
def image(filename):
    if request.method == "GET":
        return routes.post.image(filename)
    abort(405)
