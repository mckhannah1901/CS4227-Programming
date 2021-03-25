from app import Blogpost, Comment


def get_all_posts():
    return Blogpost.query.order_by(Blogpost.date.desc()).all()


def view_single_post(post_id):
    post = view_id_posts(post_id).first()
    comments = Comment.query.filter_by(id=post_id)
    return post, comments


def view_user_posts(username):
    return Blogpost.query.filter_by(username=username)


def view_id_posts(id):
    return Blogpost.query.filter_by(id=id)
