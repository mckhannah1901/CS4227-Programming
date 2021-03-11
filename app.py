
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_blog_post.db'  # update this with a different URI???
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)



class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    username = db.Column(db.Text)
    date = db.Column(db.DateTime)
    content = db.Column(db.Text)

    
api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Blogpost, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route("/addpost", methods=["GET", "POST"])
def addpost():
    if request.method == "POST":
        title = request.form['title']
        username = request.form['username']
        content = request.form['content']

        post = Blogpost(title=title, username=username,
                        content=content, date=datetime.now())

        unique_post = db.session.query(Blogpost.id).filter_by(title=title).first()

        if title == '' or username == '' or content == '':
            print("All fields of the form must be filled in!")
            render_template("addpost.html")
        elif unique_post:
            print("This title already exists, choose another!")
            render_template("addpost.html")
        else:
            db.session.add(post)
            db.session.commit()
            print("Post added!")
            return redirect(url_for("viewpost"))

    return render_template("addpost.html")


@app.route("/viewposts", methods=["GET", "POST"])
def viewpost():
    posts = Blogpost.query.order_by(Blogpost.date.desc()).all()

    return render_template('viewposts.html', posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        registration = Person(first_name=first_name, last_name=last_name,
                              email=email, username=username, password=password)

        unique_email = db.session.query(Person.id).filter_by(email=email).first()
        unique_username = db.session.query(Person.id).filter_by(username=username).first()

        if first_name == '' or last_name == '' or email == '' or username == '' or password == '':
            print("All fields of the form must be filled in!")
            render_template("register.html")
        elif unique_email:
            print("This email already exists in the database. Please choose another!")
            render_template("register.html")
        elif unique_username:
            print("This username already exists in the database. Please choose another!")
            render_template("register.html")
        else:
            db.session.add(registration)
            db.session.commit()
            print("Registration completed successfully!")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user_login = Person.query.filter_by(email=email, password=password).first()
        if user_login is not None:
            return redirect(url_for("hello_world"))
        else:
            print("Ensure a valid email/password is input!")
            render_template("login.html")
    return render_template("login.html")


if __name__ == '__main__':
    db.create_all()
    app.run()
