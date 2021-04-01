from flask_restless import APIManager
from app import db, app, login_manager
from flask_login import UserMixin

users_to_follow = db.Table(
    'users_to_follow',
    db.Column('user_following_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('user_being_followed_id', db.Integer, db.ForeignKey('person.id'))
)


class PersonManager:
    _builder = None

    def set_builder(self, builder):
        self._builder = builder

    def get_person(self):
        person = Person()

        username = self._builder.get_username()
        person.set_username(username)

        email = self._builder.get_email()
        person.set_email(email)

        password = self._builder.get_password()
        person.set_password(password)

        first_name = self._builder.get_first_name()
        person.set_first_name(first_name)

        last_name = self._builder.get_last_name()
        person.set_last_name(last_name)

        return person


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
        return self.password

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

    def __init__(self):
        self._username = None
        self._email = None
        self._password = None
        self._first_name = None
        self._last_name = None

    def set_username(self, username):
        self._username = username

    def set_email(self, email):
        self._email = email

    def set_password(self, password):
        self._password = password

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

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
