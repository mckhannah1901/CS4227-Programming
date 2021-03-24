from flask import render_template, request

from app import app, Blogpost, Comment


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


@app.route("/view-user-posts/<username>")
def view_user_posts(username):
    username_posts = Blogpost.query.filter_by(username=username)
    return render_template("view-user-posts.html", posts=username_posts)


def view_id_posts(id):
    return Blogpost.query.filter_by(id=id)
