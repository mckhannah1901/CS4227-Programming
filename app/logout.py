from flask import session, redirect, url_for

from app import app


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for("viewpost"))
