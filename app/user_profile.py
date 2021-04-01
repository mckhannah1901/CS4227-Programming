from app import app, Person, Blogpost, db, routes
from flask import redirect, url_for, session
from flask_login import current_user, login_required


@login_required
def profile_name(username):
    person = Person.query.filter_by(username=username).first()
    return person

def profile_posts(username):
    posts = Blogpost.query.filter_by(username=username).all()
    return posts