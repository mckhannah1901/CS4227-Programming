from flask import redirect, url_for, session
from flask_login import current_user, login_required

from app import Person, db, interceptor_manager
from app.models import Mediator, Log


@login_required
def follow_user(username):
    person = Person.query.filter_by(username=username).first()

    if person is None:
        log = Log('User not found within the database')
        interceptor_manager.execute(log)
        raise Exception

    if person == current_user:
        log = Log('You cannot follow yourself')
        interceptor_manager.execute(log)
        raise Exception

    current_user.follow_user(person)
    db.session.commit()

    log = Log('You are now following {}.'.format(username))
    interceptor_manager.execute(log)

    mediator = Mediator()
    mediator.notify_user(username=session['username'], email=person.email)

    return redirect(url_for('viewpost', username=username))
