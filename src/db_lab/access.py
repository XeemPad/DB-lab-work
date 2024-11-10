from functools import wraps

from flask import session, redirect, request


def login_required(func):
    @wraps(func)  # Preserves the original function's metadata and docstring.
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        
        session['next'] = request.url  # потом вернемся на предыдущую страницу
        return redirect('/auth')
    return wrapper
