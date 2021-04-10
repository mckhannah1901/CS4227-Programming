from datetime import datetime

from flask import session

from app import Blogpost, db, notifications, add_content_composite, interceptor_manager


def add_post(title, content, tag):
    username = session['username']
    person_id = session['id']

    post = Blogpost(title=title, username=username, content=content, date=datetime.now(), user_id=person_id, tag=tag)

    post_exists = db.session.query(Blogpost.id).filter_by(title=title).first()

    if title == '' or username == '' or content == '' or tag == '':
        interceptor_manager.execute("All fields of the form must be filled in!")
        raise Exception
    elif post_exists:
        interceptor_manager.execute("This title already exists, choose another!")
        raise Exception
    else:
        composite = add_content_composite.Composite()
        composite.add(post)
        pub_sub = notifications.PublisherSubscriber()
        pub_sub.notify_subscribed_users()
        interceptor_manager.execute("Post added!")
