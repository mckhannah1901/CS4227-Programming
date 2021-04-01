from flask_login import login_required

from app import Person, Blogpost


@login_required
def profile_name(username):
    person = Person.query.filter_by(username=username).first()
    return person

def profile_posts(username):
    posts = Blogpost.query.filter_by(username=username).all()
    return posts