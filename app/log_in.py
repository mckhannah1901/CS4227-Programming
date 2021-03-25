from flask import session

from app import Person


def log_in(email, password):
    user_login = Person.query.filter_by(email=email, password=password).first()
    if user_login is not None:
        session['username'] = user_login.username
        session['id'] = user_login.id
    else:
        print("Ensure a valid email/password is input!")
        raise Exception
