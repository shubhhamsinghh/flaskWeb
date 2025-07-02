import functools
from flask import session, redirect, url_for

# middleware auth
def auth(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return decorated

# middleware guest
def guest(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('tasks.view_tasks'))
        return view_func(*args, **kwargs)
    return decorated

