from flask import session

from app import Comment, db, notifications, Blogpost


def add_comment(post_id, content):
    username = session['username']
    comment = Comment(post_id=post_id, username=username, content=content)
    comment_exists = db.session.query(Comment.id).filter_by(content=content).first()

    if username == '' or content == '' or post_id == '':
        print("All fields of the form must be filled in!")
        raise Exception
    elif comment_exists:
        print("This comment already exists, choose another!")
        raise Exception
    else:
        db.session.add(comment)
        db.session.commit()
        print("Comment added.")
        post = db.session.query(Blogpost.id).filter_by(id == post_id).first()
        notifications.notify_users(post.user_id,
                                   format("New comment in post %s", post.title),
                                   format("Comment has been added to post %s", post.title))
