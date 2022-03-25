import os
import smtplib
from email.message import EmailMessage

token_dict = {}


def mail_sender(email, msg_text):
    EMAIL_ADDRESS = 'pirateshubham2115@gmail.com'
    EMAIL_PASS = '2115Shubham'

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
