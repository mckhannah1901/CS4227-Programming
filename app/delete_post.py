from app import db, Blogpost


def delete_post(postId):
    Blogpost.query.filter_by(id=postId).delete()
    db.session.commit()
