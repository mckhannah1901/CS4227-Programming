from app import db, Blogpost, notifications, Person


def delete_post(postId):
    post = Blogpost.query.filter_by(id=postId).first()
    person = db.session.query(Person.id).filter_by(username=post.username).first()

    Blogpost.query.filter_by(id=postId).delete()
    db.session.commit()

    notifications.notify_users(person.id,
                               format("Post %s deleted", post.title),
                               format("Post %s had been deleted.", post.title))
