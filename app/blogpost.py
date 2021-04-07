from app import db


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    username = db.Column(db.Text)
    date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    tag = db.Column(db.Text)
