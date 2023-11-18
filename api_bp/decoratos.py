from flask import session, render_template, redirect
from functools import wraps


def login_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if 'data' not in session:
                return render_template('index.html')
        except Exception as ex:
            if not session.get('data'):
                return redirect('/')

        return func(*args, **kwargs)

    return wrapper
