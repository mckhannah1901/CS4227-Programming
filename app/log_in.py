from flask import session
from flask_login import login_user

from app import Person, interceptor_manager


def log_in(email, password):
    user_login = Person.query.filter_by(email=email, password=password).first()
    if user_login is not None:
        session['username'] = user_login.username
        session['id'] = user_login.id
        login_user(user_login)
    else:
        interceptor_manager.execute("Ensure a valid email/password is input!")
        raise Exception
