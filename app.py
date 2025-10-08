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
    return routes.error.method_not_allowed(e)


if not app.debug:

    @app.errorhandler(Exception)
    def fallback_error(e):
        return routes.error.fallback(e)


@app.route("/", methods=["GET"])
def index():
    match request.method:
        case "GET":
            return routes.index.view()
        case _:
            abort(405)


@app.route("/favicon.<ext>", methods=["GET"])
def favicon(ext):
    match request.method:
        case "GET":
            return routes.static.favicon(ext)
        case _:
            abort(405)


@app.route("/style.css", methods=["GET"])
def style():
    match request.method:
        case "GET":
            return routes.static.style()
        case _:
            abort(405)


@app.route("/alert/clear", methods=["POST"])
def clear_alert():
    match request.method:
        case "POST":
            return routes.alert.clear()
        case _:
            abort(405)


@app.route("/register", methods=["GET", "POST"])
def register():
    match request.method:
        case "GET":
            return routes.user.create_view()
        case "POST":
            return routes.user.create()
        case _:
            abort(405)


@app.route("/login", methods=["GET", "POST"])
def login():
    match request.method:
        case "GET":
            return routes.user.login_view()
        case "POST":
            return routes.user.login()
        case _:
            abort(405)


@app.route("/logout", methods=["GET"])
def logout():
    match request.method:
        case "GET":
            return routes.user.logout()
        case _:
            abort(405)


@app.route("/user/me/edit", methods=["GET", "POST"])
def edit_user():
    match request.method:
        case "GET":
            return routes.user.edit_view()
        case "POST":
            return routes.user.update()
        case _:
            abort(405)


# @app.route("/user/me/delete", methods=["GET", "POST"])
# def delete_user():
#     match request.method:
#         case "GET":
#             return routes.user.delete_view()
#         case "POST":
#             return routes.user.delete()
#         case _:
#             abort(405)


@app.route("/me", methods=["GET"])
@app.route("/user/", methods=["GET"])
def me():
    match request.method:
        case "GET":
            return routes.user.me()
        case _:
            abort(405)


@app.route("/user/<user>", methods=["GET"])
def user_view(user):
    match request.method:
        case "GET":
            return routes.user.view(user)
        case _:
            abort(405)


@app.route("/post", methods=["GET", "POST"])
def post():
    match request.method:
        case "GET":
            return routes.post.create_view()
        case "POST":
            return routes.post.create()
        case _:
            abort(405)


@app.route("/post/", methods=["GET"])
def post_view_redirect():
    match request.method:
        case "GET":
            return redirect("/post/notfound")
        case _:
            abort(405)


@app.route("/post/<post_id>/", methods=["GET"])
def post_view_id_redirect(post_id):
    post_id = post_id.strip().lower()

    match request.method:
        case "GET":
            return redirect(f"/post/{post_id}")
        case _:
            abort(405)


@app.route("/post/<post_id>", methods=["GET"])
def post_view(post_id):
    post_id = post_id.strip().lower()

    match request.method:
        case "GET":
            return routes.post.view(post_id)
        case _:
            abort(405)


@app.route("/post/<post_id>/comment", methods=["POST"])
def comment_post(post_id):
    post_id = post_id.strip().lower()

    match request.method:
        case "POST":
            return routes.post.comment(post_id)
        case _:
            abort(405)


@app.route("/post/<post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post_id = post_id.strip().lower()

    match request.method:
        case "GET":
            return routes.post.delete_view(post_id)
        case "POST":
            return routes.post.delete(post_id)
        case _:
            abort(405)


@app.route("/post/<post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post_id = post_id.strip().lower()

    match request.method:
        case "GET":
            return routes.post.edit_view(post_id)
        case "POST":
            return routes.post.update(post_id)
        case _:
            abort(405)


@app.route("/i/", methods=["GET"])
def image_redirect():
    match request.method:
        case "GET":
            return redirect("/i/notfound")
        case _:
            abort(405)


@app.route("/i/<filename>", methods=["GET"])
def image(filename):
    match request.method:
        case "GET":
            return routes.post.image(filename)
        case _:
            abort(405)
