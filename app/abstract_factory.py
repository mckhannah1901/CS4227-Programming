from flask import session

from app import Comment, db, add_content_composite, interceptor_manager


def save_comment_to_database(post_id, content):
    username = session['username']
    comment = Comment(post_id=post_id, username=username, content=content)
    comment_exists = db.session.query(Comment.id).filter_by(content=content).first()

    if username == '' or content == '' or post_id == '':
        interceptor_manager.execute("All fields of the form must be filled in!")
        raise Exception
    elif comment_exists:
        interceptor_manager.execute("This comment already exists, choose another!")
        raise Exception
    else:
        composite = add_content_composite.Composite()
        composite.add(comment)
        interceptor_manager.execute("Comment added.")


def add_text_comment(post_id, content):
    save_comment_to_database(post_id, content)


def add_emoji_comment(post_id, content):
    save_comment_to_database(post_id, content)
