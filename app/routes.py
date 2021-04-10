from datetime import datetime

from flask import redirect, url_for
from flask import request, render_template
from flask_login import current_user

from werkzeug.urls import url_parse

from app import app, db
from app import viewposts, user_registration, log_out, log_in, add_comment, add_post, delete_post, edit_post, \
    user_subscribing, user_profile


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home-page.html")


@app.route('/profile/<username>', methods=['GET', 'POST'])
def view_user_profile(username):
    if request.method == "GET":
        person = user_profile.profile_name(username)
        posts = user_profile.profile_posts(username)
        return render_template("user-profile-page.html", person=person, posts=posts)


@app.route('/user_subscribe/<username>', methods=['GET', 'POST'])
def subscribe_to_user(username):
    try:
        return redirect(url_for("viewpost", username=user_subscribing.follow_user(username)))
    except Exception as ex:
        return redirect(url_for('viewpost'))


@app.route("/viewposts", methods=["GET", "POST"])
def viewpost():
    if request.method == "GET":
        return render_template('viewposts.html', posts=viewposts.get_all_posts())


@app.route("/viewposts/<tag>", methods=["GET", "POST"])
def viewtaggedpost(tag):
    if request.method == "GET":
        return render_template('viewposts.html', posts=viewposts.get_tagged_posts(tag))


@app.route("/view-post/<string:post_id>", methods=["GET", "POST"])
def view_single_post(post_id):
    if request.method == "GET":
        post, comments = viewposts.view_single_post(post_id)
        return render_template('view-single-post.html', post=post, comments=comments)


@app.route("/view-user-posts/<username>")
def view_user_posts(username):
    return render_template("view-user-posts.html", posts=viewposts.view_user_posts(username))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user_registration.register_new_user(request.form['first_name'], request.form['last_name'],
                                                request.form['email'], request.form['username'],
                                                request.form['password'])
            return redirect(url_for("login"))
        except Exception as ex:
            return render_template("register.html")
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/logout")
def logout():
    log_out.log_out()
    return redirect(url_for("viewpost"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            log_in.log_in(request.form['email'], request.form['password'])
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('viewpost')
            return redirect(next_page)
        except Exception as ex:
            return render_template("login.html")
    elif request.method == "GET":
        return render_template("login.html")


@app.route("/add-reaction/<post_id>", methods=["GET", "POST"])
def addreaction(post_id):
    if request.method == "POST":
        try:
            add_comment.add_comment(post_id, request.form['content'], "emoji")
            return redirect(url_for("view_single_post", post_id=post_id))
        except Exception as ex:
            return render_template("add-reaction.html")
    elif request.method == "GET":
        return render_template("add-reaction.html")


@app.route("/add-comment/<post_id>", methods=["GET", "POST"])
def addcomment(post_id):
    if request.method == "POST":
        try:
            add_comment.add_comment(post_id, request.form['content'], "text")
            return redirect(url_for("view_single_post", post_id=post_id))
        except Exception as ex:
            return render_template("add-comment.html")
    elif request.method == "GET":
        return render_template("add-comment.html")


@app.route("/addpost", methods=["GET", "POST"])
def addpost():
    if request.method == "POST":
        try:
            add_post.add_post(request.form['title'], request.form['content'], request.form['tag'])
            return redirect(url_for("viewpost"))
        except Exception as ex:
            return render_template("addpost.html")
    elif request.method == "GET":
        return render_template("addpost.html")


@app.route("/delete/<id>/<username>", methods=["GET"])
def deletepost(id, username):
    delete_post.delete_post(id)
    return view_user_posts(username)


@app.route("/edit/<id>/<username>", methods=["GET", "POST"])
def editpost(id, username):
    if request.method == "POST":
        edit_post.edit_post(id)
        return redirect(url_for("view_user_posts", username=username))
    elif request.method == "GET":
        return render_template("edit-post.html")
