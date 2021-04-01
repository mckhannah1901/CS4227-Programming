from flask_mail import Message

import app


def notify_subscription_event(email, subject, body):
    msg = Message(subject=subject,
                  sender=app.mail_settings.get("MAIL_USERNAME"),
                  recipients=[email],
                  body=body)
    app.mail.send(msg)
