from functools import wraps
from flask import request, current_app
from helpscout import is_helpscout_request


def signed_request(f):
    """Checks that an incoming request originates from Help Scout."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        helpscout_sig =  request.headers.get('X-Helpscout-Signature')
        secret = current_app.config.get('HELPSCOUT_SECRET')

        if not is_helpscout_request(secret, request.data, helpscout_sig):
            return '', 400

        return f(*args, **kwargs)
    return decorated_function
