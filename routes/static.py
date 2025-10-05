from os import path

from flask import abort, send_from_directory

__all__ = [
    "favicon",
    "style",
]


FAVICON_TYPES = {
    "ico": "image/vnd.microsoft.icon",
    "png": "image/png",
    "svg": "image/svg+xml",
}


def favicon(ext="ico"):
    if ext not in FAVICON_TYPES.keys():
        abort(404)

    return send_from_directory(
        path.join("static", "images"),
        f"favicon.{ext}",
        mimetype=FAVICON_TYPES[ext],
    )


def style():
    return send_from_directory(
        path.join("static"),
        "style.css",
        mimetype="text/css",
    )
