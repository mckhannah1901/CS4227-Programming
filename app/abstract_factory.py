from flask import session

from app import Comment, db


def save_comment_to_database(post_id, content):
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


def add_text_comment(post_id, content):
    save_comment_to_database(post_id, content)


def add_emoji_comment(post_id, content):
    save_comment_to_database(post_id, content)
