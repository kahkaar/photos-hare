from flask import redirect, render_template, request, send_from_directory

import api
from routes.helpers import alert, csrf, jpeg
from routes.helpers import session as sesh
from routes.helpers import to_localtime

from . import helpers

__all__ = [
    "create",
    "create_view",
    "delete",
    "image",
    "update",
    "view",
]


def create():
    csrf.validate()
    sesh.require_login()

    title = request.form.get("title", "", str).strip()
    description = request.form.get("description", "", str).strip()
    unlisted = bool(request.form.get("unlisted", False, bool))
    file = request.files.get("file", None)

    if not helpers.is_title_valid(title):
        alert.set("ERROR: title is not valid")
        return redirect("/post")

    if not helpers.is_description_valid(description):
        alert.set("ERROR: description is not valid")
        return redirect("/post")

    if not file:
        alert.set("ERROR: file not found")
        return redirect("/post")

    data = file.read()

    max_size_kb = 500
    max_size_bytes = max_size_kb * 1024

    if len(data) > max_size_bytes:
        alert.set(f"ERROR: file size too big (max {max_size_bytes} bytes)")
        return redirect("/post")

    if not jpeg.validate_signature(data):
        alert.set("ERROR: file is not valid, must be (.jpg, .jpeg)")
        return redirect("/post")

    result = api.posts.create(title, description, unlisted)
    # post_id = None if not result and "id" not in result else result["id"]
    post_id = result["id"]

    if not post_id:
        alert.set("ERROR: post could not be returned")
        return redirect("/post")

    jpeg.save(data, post_id)
    api.posts.update_filename(post_id, f"{post_id}.jpg")

    return redirect(f"/post/{post_id}")


def create_view():
    if not sesh.validate():
        return redirect("/login")

    csrf.init()
    return render_template("post_form.html")


def delete(post_id):
    sesh.require_login()
    csrf.validate()

    post = api.posts.get(post_id)
    sesh.require_ownership(post)

    api.posts.delete(post_id)
    helpers.delete_image(post["filename"])

    alert.set(f"Deleted {post['title']}")

    return redirect("/")


def delete_view(post_id):
    if not sesh.validate():
        return redirect(f"/post/{post_id}")

    post = api.posts.get(post_id)

    if not sesh.is_owner(post):
        return redirect(f"/post/{post_id}")

    post = to_localtime(post)

    csrf.init()
    return render_template("delete_post_form.html", post=post)


def edit_view(post_id):
    if not sesh.validate():
        return redirect(f"/post/{post_id}")

    post = api.posts.get(post_id)

    if not sesh.is_owner(post):
        return redirect(f"/post/{post_id}")

    post = to_localtime(post)

    csrf.init
    return render_template("edit_post_form.html", post=post)


def image(filename):
    return send_from_directory("uploads", filename)


def update(post_id):
    sesh.require_login()
    csrf.validate()

    post = api.posts.get(post_id)
    sesh.require_ownership(post)

    description = post["description"]
    unlisted = post["unlisted"]

    new_desc = request.form.get("description", description, str).strip()
    new_unlisted = bool(request.form.get("unlisted", unlisted, bool))

    desc_changed = description != new_desc
    unlisted_changed = unlisted != new_unlisted

    message = "Post was not edited"
    if desc_changed or unlisted_changed:
        api.posts.update(post_id, new_desc, new_unlisted)

        message = f"Edited description and listing status ({'unlisted' if new_unlisted else 'listed'})"
        if desc_changed and not unlisted_changed:
            message = "Post has a new description"
        elif not desc_changed and unlisted_changed:
            message = (
                "Post is now unlisted (direct links still show post)"
                if new_unlisted
                else "Post is now publicly listed"
            )

    alert.set(message)
    return redirect(f"/post/{post_id}")


def view(post_id):
    post = to_localtime(api.posts.get(post_id))
    return render_template("post.html", post=post)
