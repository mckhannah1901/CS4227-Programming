from flask import request, render_template, redirect, url_for

from app import app, Comment, db


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
