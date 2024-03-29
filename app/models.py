from flask_login import UserMixin
from flask_restless import APIManager

from app import db, app, login_manager, notifications
from app.blogpost import Blogpost
from app.comment import Comment

users_to_follow = db.Table(
    'users_to_follow',
    db.Column('user_following_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('user_being_followed_id', db.Integer, db.ForeignKey('person.id'))
)


class Log:
    _message = None

    def __init__(self, message):
        self._message = message

    def log(self):
        print(self._message)


class Mediator(object):
    def notify_user(self, username, email):
        subject = "New user has subscribed to you"
        body = "User {username} has subscribed to you. They can see any activity you have.".format(
            username=username)

        pub_sub = notifications.PublisherSubscriber()
        pub_sub.notify_subscription_event(email=email, subject=subject, body=body)


class Memento:
    def __init__(self, post):
        self.post = post


class PostEditUtility:
    def __init__(self, post):
        self.post = post

    def edit(self, new_post):
        self.post = new_post

    def save(self):
        return Memento(self.post)

    def undo(self, memento):
        self.post = memento.post


class PostEditCaretaker:
    def save(self, edit_utility):
        self.obj = edit_utility.save()

    def undo(self, edit_utility):
        edit_utility.undo(self.obj)


class PersonManager:
    _builder = None

    def set_builder(self, builder):
        self._builder = builder

    def get_person(self):
        username = self._builder.get_username()
        email = self._builder.get_email()
        password = self._builder.get_password()
        first_name = self._builder.get_first_name()
        last_name = self._builder.get_last_name()

        print(username, email, password, first_name, last_name)

        registration = Person(first_name=first_name, last_name=last_name, email=email, username=username,
                              password=password)

        return registration


class Builder:
    def get_username(self): pass

    def get_email(self): pass

    def get_password(self): pass

    def get_first_name(self): pass

    def get_last_name(self): pass


class PersonBuilder(Builder):
    username = None
    email = None
    password = None
    first_name = None
    last_name = None

    def set_variables(self, username, email, password, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name


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


api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Blogpost, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Comment, methods=['GET', 'POST', 'DELETE', 'PUT'])
db.create_all()
