from threading import Thread
from typing import List

from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.models import User


def send_email(subject: str, sender: str, recipients: List[str] | str, text_body: str, html_body: str):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_email('[KursoAgreagator] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))