import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
import redis
import json

token_dict = {}


r = redis.Redis(
    host='localhost',
    port=6379
)

def mail_sender(email, msg_text):
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = 'Activate Account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f"{msg_text}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)


def url_short(token):
    key = len(token_dict) + 1
    token_dict.__setitem__(key, token)
    return key

def do_cache(key, value, expire_time):
    json_dict = json.dumps(value)
    r.set(key, json_dict)
    r.expire(key, expire_time)


def get_cache(key):
    value = r.get(key)
    return value