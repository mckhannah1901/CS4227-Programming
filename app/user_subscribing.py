from flask import redirect, url_for
from flask_login import current_user, login_required

from app import Person, db
from app.models import Mediator


@login_required
def follow_user(username):
    person = Person.query.filter_by(username=username).first()

    if person is None:
        print('User not found within the database')
        return redirect(url_for('viewpost'))

    if person == current_user:
        print('You cannot follow yourself')
        return redirect(url_for('viewpost', username=username))

    current_user.follow_user(person)
    db.session.commit()
    print('You are now following {}.'.format(username))

    mediator = Mediator()
    mediator.notify_user(username=person.username, email=person.email)

    return redirect(url_for('viewpost', username=username))
