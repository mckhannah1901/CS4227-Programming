from flask import redirect, url_for, session
from flask_login import current_user, login_required

from app import Person, db, interceptor_manager
from app.models import Mediator


@login_required
def follow_user(username):
    person = Person.query.filter_by(username=username).first()

    if person is None:
        interceptor_manager.execute('User not found within the database')
        return redirect(url_for('viewpost'))

    if person == current_user:
        interceptor_manager.execute('You cannot follow yourself')
        return redirect(url_for('viewpost', username=username))

    current_user.follow_user(person)
    db.session.commit()
    interceptor_manager.execute('You are now following {}.'.format(username))

    mediator = Mediator()
    mediator.notify_user(username=session['username'], email=person.email)

    return redirect(url_for('viewpost', username=username))
