from flask_restless import APIManager
from app import db, app, login_manager
from flask_login import UserMixin

users_to_follow = db.Table(
    'users_to_follow',
    db.Column('user_following_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('user_being_followed_id', db.Integer, db.ForeignKey('person.id'))
)


class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    followed_user = db.relationship(
        'Person', secondary=users_to_follow,
        primaryjoin=(users_to_follow.c.user_following_id == id),
        secondaryjoin=(users_to_follow.c.user_being_followed_id == id),
        backref=db.backref('users_to_follow', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Person {}>'.format(self.username)

    def follow_user(self, person):
        if not self.is_following_user(person):
            self.followed_user.append(person)

    def unfollow_user(self, person):
        if self.is_following_user(person):
            self.followed_user.remove(person)

    def is_following_user(self, person):
        return self.followed_user.filter(
            users_to_follow.c.user_being_followed_id == person.id).count() > 0


@login_manager.user_loader
def user_loader(id):
    return Person.query.get(int(id))


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    username = db.Column(db.Text)
    date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    tag = db.Column(db.Text)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    username = db.Column(db.Text)
    date = db.Column(db.Text)
    content = db.Column(db.Text)


api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Blogpost, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Comment, methods=['GET', 'POST', 'DELETE', 'PUT'])
db.create_all()
