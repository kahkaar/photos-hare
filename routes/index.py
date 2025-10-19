from flask import render_template, request, session

import api
from routes.helpers import csrf, to_localtime

__all__ = ["view"]


def view():
    csrf.init()
    query = request.args.get("q", "", str)
    session["query"] = query.strip()

    amount = request.args.get("a", 10, int)
    page = request.args.get("p", 1, int)

    limit = amount
    offset = (page - 1) * amount

    posts = (
        api.posts.find(query, limit, offset)
        if query
        else api.posts.get_all(limit, offset)
    )

    posts = [to_localtime(post) for post in posts]

    return render_template("index.html", posts=posts, amount=amount, page=page)
