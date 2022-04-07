import os
import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from common import utils


def get_token(user_name):
    token = jwt.encode({'User': user_name, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=600))},
                       str(os.environ.get('SECRET_KEY')))
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            short_token = request.headers.get('access-token')
        else:
            short_token = request.args.get('token')
        token = utils.token_dict[int(short_token)]
        if not token:
            return jsonify(message='Token is missing!')
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
        except:
            return jsonify(message='Token is invalid')

        return f(data['User'])

    return decorated
