from datetime import datetime

from flask import render_template, request, redirect, url_for, session
from sqlalchemy.orm.attributes import flag_modified

from app import db, app
from app.models import Person, Blogpost, Comment


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
            session['username'] = user_login.username
            session['id'] = user_login.id
            print(session['username'], session['id'])
            return redirect(url_for("viewpost"))
        else:
            print("Ensure a valid email/password is input!")
            render_template("login.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for("viewpost"))


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


@app.route("/view-post/<string:post_id>", methods=["GET", "POST"])
def view_single_post(post_id):
    if request.method == "GET":
        post = Blogpost.query.filter_by(id=post_id).first()
        comments = Comment.query.filter_by(id=post_id)
        return render_template('view-single-post.html', post=post, comments=comments)


@app.route("/add-comment/<post_id>", methods=["GET", "POST"])
def add_comment(post_id):
    if request.method == "POST":
        username = request.form['username']
        content = request.form['content']
        comment = Comment(post_id=post_id, username=username, content=content)
        unique_comment = db.session.query(Comment.id).filter_by(content=content).first()

        if username == '' or content == '' or post_id == '':
            print("All fields of the form must be filled in!")
            render_template("add-comment.html")
        elif unique_comment:
            print("This title already exists, choose another!")
            render_template("add-comment.html")
        else:
            db.session.add(comment)
            db.session.commit()
            print("Comment added.")
            return redirect(url_for("view_single_post", post_id=post_id))

    else:
        return render_template("add-comment.html")


@app.route("/view-user-posts/<username>")
def view_user_posts(username):
    username_posts = Blogpost.query.filter_by(username=username)
    return render_template("view-user-posts.html", posts=username_posts)


def view_id_posts(id):
    return Blogpost.query.filter_by(id=id)


@app.route("/delete/<id>/<username>", methods=["GET"])
def delete(id, username):
    Blogpost.query.filter_by(id=id).delete()
    db.session.commit()
    return view_user_posts(username)


@app.route("/edit/<id>/<username>", methods=["GET", "POST"])
def edit(id, username):
    if request.method == "POST":
        original_blog_post_data = Blogpost.query.filter_by(id=id)[0]

        new_blog_post_data = get_blog_post_data(id)

        original_blog_post_data.title = new_blog_post_data.title
        original_blog_post_data.username = new_blog_post_data.username
        original_blog_post_data.date = new_blog_post_data.date
        original_blog_post_data.content = new_blog_post_data.content

        flag_modified(original_blog_post_data, "title")
        flag_modified(original_blog_post_data, "date")
        flag_modified(original_blog_post_data, "username")
        flag_modified(original_blog_post_data, "content")

        db.session.merge(original_blog_post_data)
        db.session.flush()
        db.session.commit()

        return redirect(url_for("view_user_posts", username=username))
    elif request.method == "GET":
        return render_template("edit-post.html")


def get_blog_post_data(id):
    title = request.form['title']
    username = request.form['username']
    content = request.form['content']

    post = Blogpost(id=id, title=title, username=username,
                    content=content, date=datetime.now())

    return post