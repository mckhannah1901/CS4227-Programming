from app import app, Person, Blogpost, db, routes
from flask import redirect, url_for, session
from flask_login import current_user, login_required


@app.route('/user_subscribe/<username>', methods=['GET', 'POST'])
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
    return redirect(url_for('viewpost', username=username))
