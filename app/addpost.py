from datetime import datetime

from flask import request, render_template, redirect, url_for

from app import app, Blogpost, db


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
