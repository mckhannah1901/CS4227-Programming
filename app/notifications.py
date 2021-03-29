from flask_mail import Message

from app import Person, db, mail


def notify_users(user_id, subject, body):
    person = db.session.query(Person.id).filter_by(id == user_id).first()
    person_subbed_person = person.followed_user

    for p in person_subbed_person:
        subbed_person = db.session.query(Person.id).filter_by(id == p.id).first()
        print(subbed_person.email)
        msg = Message(subject=subject, body=body)
        mail.send(msg)
