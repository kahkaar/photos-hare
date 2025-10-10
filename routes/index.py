from flask import render_template, request, session

import api
from routes.helpers import csrf, to_localtime

__all__ = ["view"]


def view():
    csrf.init()
    query = request.args.get("q", "", str)
    session["query"] = query.strip()

    posts = api.posts.find(query) if query else api.posts.get_all()
    users = api.users.get_all()

    posts = [to_localtime(post) for post in posts]

    return render_template("index.html", posts=posts, users=users)
