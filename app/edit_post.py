from datetime import datetime

from flask import request
from sqlalchemy.orm.attributes import flag_modified

from app import Blogpost, db


def edit_post(post_id):
    original_blog_post_data = Blogpost.query.filter_by(id=post_id)[0]

    new_blog_post_data = get_blog_post_data(post_id)

    original_blog_post_data.title = new_blog_post_data.title
    original_blog_post_data.username = new_blog_post_data.username
    original_blog_post_data.date = new_blog_post_data.date
    original_blog_post_data.content = new_blog_post_data.content

    flag_modified(original_blog_post_data, "title")
    flag_modified(original_blog_post_data, "date")
    flag_modified(original_blog_post_data, "username")
    flag_modified(original_blog_post_data, "content")

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
