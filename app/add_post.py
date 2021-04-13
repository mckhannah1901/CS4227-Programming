from datetime import datetime

from flask import session

from app import Blogpost, db, notifications, add_content_composite, interceptor_manager
from app.models import Log


def add_post(title, content, tag):
    username = session['username']
    person_id = session['id']

    post = Blogpost(title=title, username=username, content=content, date=datetime.now(), user_id=person_id, tag=tag)

    post_exists = db.session.query(Blogpost.id).filter_by(title=title).first()

    if title == '' or username == '' or content == '' or tag == '':
        log = Log("All fields of the form must be filled in!")
        interceptor_manager.execute(log)
        raise Exception
    elif post_exists:
        log = Log("This title already exists, choose another!")
        interceptor_manager.execute(log)
        raise Exception
    else:
        composite = add_content_composite.Composite()
        composite.add(post)
        pub_sub = notifications.PublisherSubscriber()
        pub_sub.notify_subscribed_users()
        log = Log("Post added!")
        interceptor_manager.execute(log)
