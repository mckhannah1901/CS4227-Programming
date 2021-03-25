from app import db, app, Blogpost
from app.viewposts import view_user_posts


@app.route("/delete/<id>/<username>", methods=["GET"])
def delete(id, username):
    Blogpost.query.filter_by(id=id).delete()
    db.session.commit()
    return view_user_posts(username)
