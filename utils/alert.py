from flask import session


def set(message):
    session["alert"] = message


def clear():
    if "alert" in session:
        del session["alert"]
