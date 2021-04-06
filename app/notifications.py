from flask import session
from flask_mail import Message

from app import mail, models


class PublisherSubscriber:
    def notify_subscription_event(self, email, subject, body):
        msg = Message(subject, sender='cs4227.blog.website@gmail.com', recipients=[email])
        msg.body = body
        mail.send(msg)

    def notify_subscribed_users(self):
        username = session['username']
        person = models.Person.query.filter_by(username=username).first()

        all_people = models.Person.query.all()

        for p in all_people:
            subbed_users = p.followed_user.all()
            person_id = int(person.id)

            person_identifiers = []

            for sub in subbed_users:
                person_identifiers.append(sub.id)

            if person_id in person_identifiers:
                self.notify_subscription_event(p.email, "New Subject", "There was a new post created.")
            else:
                continue
