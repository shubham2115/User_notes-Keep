import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
load_dotenv()
import redis
import json

token_dict = {}


r = redis.Redis(
    host='localhost',
    port=6379
)

def get_token(user_name):
    token = jwt.encode({'User': user_name, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=60000))},
                       str(os.environ.get('SECRET_KEY')))
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            short_token = request.headers.get('access-token')
        else:
            short_token = request.args.get('token')
        token = token_dict[int(short_token)]
        if not token:
            return jsonify(message='Token is missing!')
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
        except:
             return jsonify(message='Token is invalid')

        return f(data['User'])

    return decorated


def mail_sender(email, template):
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    msg = MIMEMultipart()
    msg['Subject'] = 'Activate Account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    # msg.set_content(f"{msg_text}")
    msg.attach(MIMEText(template,'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)


def url_short(token):
    key = len(token_dict) + 1
    token_dict.__setitem__(key, token)
    return key

def set_cache(key, value, expire_time):
    json_dict = json.dumps(value)
    r.set(key, json_dict)
    r.expire(key, expire_time)


def get_cache(key):
    value = r.get(key)
    return value