from app import db, Comment, Blogpost, interceptor_manager


class Content:
    def add(self, content):
        pass


class CommentAdder(Content):
    def add(self, content):
        db.session.add(content)
        db.session.commit()


class BlogpostAdder(Content):
    def add(self, content):
        db.session.add(content)
        db.session.commit()


class Composite(Content):
    def add(self, content):
        if isinstance(content, Comment):
            ca = CommentAdder()
            ca.add(content)
        elif isinstance(content, Blogpost):
            ba = BlogpostAdder()
            ba.add(content)
        else:
            interceptor_manager.execute("This is not a compatible object for this.")
