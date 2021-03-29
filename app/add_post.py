from datetime import datetime

from flask import session

from app import Blogpost, db, notifications, Person


def add_post(title, content):
    username = session['username']
    person_id = session['id']

    post = Blogpost(title=title, username=username, content=content, date=datetime.now(), user_id=person_id)

    post_exists = db.session.query(Blogpost.id).filter_by(title=title).first()

    if title == '' or username == '' or content == '':
        print("All fields of the form must be filled in!")
        raise Exception
    elif post_exists:
        print("This title already exists, choose another!")
        raise Exception
    else:
        db.session.add(post)
        db.session.commit()
        print("Post added!")
        person = db.session.query(Person.id).filter_by(id == person_id).first()
        notifications.notify_users(person_id,
                                   format("New post by %s", person.username),
                                   format("Post has been created by %s.", person.username))
