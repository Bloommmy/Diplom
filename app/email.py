from flask_mail import Message
from app import mail
from flask import render_template
from app import app

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Отдел Маркетинга СПбГЭТУ "ЛЭТИ"] Сброс пароля',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_new_user(FullName, email, username, parol):
    send_email('[Отдел Маркетинга СПбГЭТУ "ЛЭТИ"] Успешная регистрация',
                sender=app.config['ADMINS'][0],
                recipients=[email],
                text_body=render_template('email/new_user.txt',
                                          FullName=FullName, username=username, parol=parol),
                html_body=render_template('email/new_user.html',
                                          FullName=FullName, username=username, parol=parol))
    return 1
