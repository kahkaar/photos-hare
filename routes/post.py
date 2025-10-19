from flask import (
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
from werkzeug.datastructures.file_storage import FileStorage

import api
from routes.helpers import alert, csrf, jpeg, to_localtime
from routes.helpers import session as sesh

from . import helpers

__all__ = [
    "comment",
    "create",
    "create_view",
    "delete",
    "image",
    "like",
    "update",
    "view",
]


def comment(post_id):
    csrf.validate()
    if not sesh.has_session():
        return redirect(f"/post/{post_id}")

    message = request.form.get("comment", "", str).strip()

    if not helpers.is_comment_valid(message):
        errors = ["comment is either too short or too long"]
        return helpers.redirect_with_errors("/post", errors)

    user_id = session["user_id"]

    new_comment = api.comments.create(message, post_id, user_id)

    return redirect(f"/post/{post_id}#{new_comment['id']}")


def create():
    csrf.validate()
    sesh.require_session()

    title = request.form.get("title", "", str).strip()
    description = request.form.get("description", "", str).strip()
    unlisted = bool(request.form.get("unlisted", False, bool))
    tag = request.form.get("tags", "", str).strip().lower()
    file = request.files.get("file", FileStorage())

    errors = set()
    is_valid = True
    if not helpers.is_title_valid(title):
        errors.add("title is not valid")
        is_valid = False

    if not helpers.is_description_valid(description):
        errors.add("description is not valid")
        is_valid = False

    if not file:
        errors.add("file not found")
        is_valid = False

    if not is_valid:
        return helpers.redirect_with_errors("/post", errors)

    data = file.read()

    max_size_kb = 500
    max_size_bytes = max_size_kb * 1024

    if len(data) > max_size_bytes:
        errors.add(f"file size too big (max {max_size_bytes} bytes)")
        is_valid = False

    if not jpeg.validate_signature(data):
        errors.add("file is not valid (must be .jpg, .jpeg)")
        is_valid = False

    if not is_valid:
        return helpers.redirect_with_errors("/post", errors)

    user_id = session["user_id"]
    result = api.posts.create(user_id, title, description, unlisted)
    post_id = result["id"]

    if not post_id:
        errors.add("post could not be returned")
        is_valid = False

    if not is_valid:
        return helpers.redirect_with_errors("/post", errors)

    if tag:
        api.tags.insert(post_id, tag)

    jpeg.save(data, post_id)
    api.posts.update_filename(post_id, f"{post_id}.jpg")

    return redirect(f"/post/{post_id}")


def create_view():
    if not sesh.has_session():
        return redirect("/login")

    tags = api.tags.get_all()

    csrf.init()
    return render_template("post_form.html", tags=tags)


def delete(post_id):
    sesh.require_session()
    csrf.validate()

    if "cancel" in request.form:
        return redirect(f"/post/{post_id}")

    post = api.posts.get(post_id)
    sesh.require_ownership(post)

    api.posts.delete(post_id)
    helpers.delete_image(post["filename"])

    alert.set(f"Deleted {post['title']}")

    return redirect("/")


def delete_view(post_id):
    if not sesh.has_session():
        return redirect(f"/post/{post_id}")

    post = api.posts.get(post_id)

    if not sesh.is_owner(post):
        return redirect(f"/post/{post_id}")

    post = to_localtime(post)

    csrf.init()
    return render_template("delete_post_form.html", post=post)


def edit_view(post_id):
    if not sesh.has_session():
        return redirect(f"/post/{post_id}")

    post = api.posts.get(post_id)

    if not sesh.is_owner(post):
        return redirect(f"/post/{post_id}")

    post = to_localtime(post)

    tags = api.tags.get_all()

    csrf.init()
    return render_template("edit_post_form.html", post=post, tags=tags)


def image(filename):
    return send_from_directory("uploads", filename)


def like(post_id):
    sesh.require_session()
    csrf.validate()

    user_id = session["user_id"]
    type = "like" in request.form

    comment_id = request.args.get("c", "").strip().lower()
    if comment_id:
        api.comments.like(comment_id, user_id, type)
        return redirect(f"/post/{post_id}#{comment_id}")

    api.posts.like(post_id, user_id, type)

    return redirect(f"/post/{post_id}")


def update(post_id):
    sesh.require_session()
    csrf.validate()

    if "cancel" in request.form:
        return redirect(f"/post/{post_id}")

    if "delete" in request.form:
        return redirect(f"/post/{post_id}/delete")

    post = api.posts.get(post_id)
    sesh.require_ownership(post)

    description = post["description"]
    unlisted = post["unlisted"]
    tag = post["tag_id"]

    new_desc = request.form.get("description", "", str).strip()
    new_unlisted = bool(request.form.get("unlisted", False, bool))
    new_tag = request.form.get("tags", "", str).strip().lower()

    desc_changed = description != new_desc
    unlisted_changed = unlisted != new_unlisted
    tag_changed = tag != new_tag

    message = ["Post was not edited"]
    if desc_changed or unlisted_changed or tag_changed:
        api.posts.update(post_id, new_desc, new_unlisted)

        message = []

        if desc_changed:
            message.append("description updated")

        if unlisted_changed:
            status = "unlisted" if new_unlisted else "listed"
            message.append(f"listing status updated ({status})")

        if tag_changed:
            api.tags.delete_from_post(post_id, tag)
            api.tags.insert(post_id, new_tag)
            message.append("tag updated")

    alert.set(", ".join(message))
    return redirect(f"/post/{post_id}")


def view(post_id):
    amount = request.args.get("a", 10, int)
    page = request.args.get("p", 1, int)

    limit = amount
    offset = (page - 1) * amount

    post = to_localtime(api.posts.get(post_id))
    comments = [
        to_localtime(c) for c in api.comments.get_of(post_id, limit, offset)
    ]

    return render_template(
        "post.html", post=post, comments=comments, amount=amount, page=page
    )
