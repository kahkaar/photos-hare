from flask import session

__all__ = [
    "clear",
    "set",
]


def clear():
    if "alert" in session:
        del session["alert"]


def set(message):
    session["alert"] = message
