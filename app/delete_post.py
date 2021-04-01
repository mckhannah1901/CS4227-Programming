from app import db, Blogpost, Person


def delete_post(postId):
    post = Blogpost.query.filter_by(id=postId).first()
    person = db.session.query(Person.id).filter_by(username=post.username).first()

    Blogpost.query.filter_by(id=postId).delete()
    db.session.commit()
