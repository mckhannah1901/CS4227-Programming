from datetime import datetime

from flask import request
from sqlalchemy.orm.attributes import flag_modified

from app import Blogpost, db


def edit_post(post_id):
    original_blog_post_data = Blogpost.query.filter_by(id=post_id)[0]
    existing_blog_post_data = original_blog_post_data
    new_blog_post_data = get_blog_post_data(post_id)

    editor = models.PostEditUtility(original_blog_post_data)

    try:
        existing_blog_post_data.title = new_blog_post_data.title
        existing_blog_post_data.username = new_blog_post_data.username
        existing_blog_post_data.date = new_blog_post_data.date
        existing_blog_post_data.content = new_blog_post_data.content

        editor.edit(new_blog_post_data)

        flag_modified(existing_blog_post_data, "title")
        flag_modified(existing_blog_post_data, "date")
        flag_modified(existing_blog_post_data, "username")
        flag_modified(existing_blog_post_data, "content")

        db.session.merge(existing_blog_post_data)
        db.session.flush()
        db.session.commit()
    except Exception as ex:
        edit_caretaker.undo(editor)
        db.session.merge(original_blog_post_data)
        db.session.flush()
        db.session.commit()


def get_blog_post_data(id):
    title = request.form['title']
    username = request.form['username']
    content = request.form['content']

    post = Blogpost(id=id, title=title, username=username,
                    content=content, date=datetime.now())

    return post
