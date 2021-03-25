from app import viewposts, app

from flask import render_template, request


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
