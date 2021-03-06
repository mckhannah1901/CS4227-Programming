from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # update this with a different URI???
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    date = db.column(db.DATETIME)
    content = db.column(db.Text)


db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/')
def hello_world():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('home-page.html', posts=posts)


if __name__ == '__main__':
    app.run()
