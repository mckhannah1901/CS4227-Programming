from flask import request, render_template

from flask import session, redirect, url_for

from app import app
from app import viewposts, user_registration, log_out

from flask import redirect, url_for


@app.route("/viewposts", methods=["GET", "POST"])
def viewpost():
    if request.method == "GET":
        return render_template('viewposts.html', posts=viewposts.get_all_posts())


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
            user_registration.register_new_user(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['username'], request.form['password'])
            return redirect(url_for("login"))
        except Exception as ex:
            print(ex)
            return render_template("register.html")
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/logout")
def logout():
    log_out.log_out()
    return redirect(url_for("viewpost"))



