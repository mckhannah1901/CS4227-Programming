from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    username = db.Column(db.Text)
    date = db.Column(db.Text)
    content = db.Column(db.Text)
