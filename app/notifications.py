from flask_mail import Message

from app import mail


def notify_subscription_event(email, subject, body):
    msg = Message(subject, sender='cs4227.blog.website@gmail.com', recipients=[email])
    msg.body = body
    mail.send(msg)
