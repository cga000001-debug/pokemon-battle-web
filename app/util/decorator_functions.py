from functools import wraps
from flask import redirect, session, url_for


def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer" not in session:
            return redirect(url_for("user.index"))
        return func(*args, **kwargs)
    return wrapper
