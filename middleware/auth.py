from functools import wraps,WRAPPER_UPDATES
from flask import session


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
        return f(*args, **kwargs)

    return decorated
