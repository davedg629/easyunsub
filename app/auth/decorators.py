from flask import flash, session, redirect, url_for
from functools import wraps


# login required wrapper
def admin_login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Please login.')
            return redirect(url_for('auth.admin_login'))
    return wrap


# for views that don't require admin login
def public_endpoint(function):
    function.is_public = True
    return function
