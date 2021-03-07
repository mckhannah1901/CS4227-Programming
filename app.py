from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect
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
    username = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    content = db.column(db.Text)


api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Blogpost, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route("/addpost", methods=["GET", "POST"])
def addpost():
    if request.method == "POST":
        title = request.form['title']
        username = request.form['username']
        content = request.form['content']

        post = Person(title=title, username=username,
                              content=content, datetime = datetime.now())

        unique_post = db.session.query(Person.id).filter_by(title=title).first()

        if title == '' or username == '' or content == '':
            print("All fields of the form must be filled in!")
            render_template("addpost.html")
        elif unique_post:
            print("This email already exists in the database. Please choose another!")
            render_template("addpost.html")
        else:
            db.session.add(post)
            db.session.commit()
            print("Registration completed successfully!")
            return redirect(url_for("post-viewer"))

    return render_template("addpost.html")


if __name__ == '__main__':
    db.create_all()
    app.run()
