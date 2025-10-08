from flask import jsonify, render_template
from werkzeug.exceptions import HTTPException

__all__ = [
    "fallback",
    "forbidden",
    "method_not_allowed",
    "not_found",
]


def fallback(e):
    code = 500
    error = "Unexpected error occurred"

    if isinstance(e, HTTPException):
        code = e.code if e.code else code
        error = e.description

    return render_template(
        "error.html",
        code=code,
        error=error,
    ), code


def forbidden(e):
    return render_template("403.html", error=e), 403


def method_not_allowed():
    return jsonify({"error": "Method not allowed"}), 405


def not_found(e):
    return render_template("404.html", error=e), 404
