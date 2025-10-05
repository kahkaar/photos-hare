from flask import redirect, request

from routes.helpers import alert, csrf

__all__ = ["clear"]


def clear():
    csrf.validate()
    alert.clear()
    return redirect(request.referrer)
