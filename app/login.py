from flask import request, session, redirect, url_for, render_template

from app import app, Person


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user_login = Person.query.filter_by(email=email, password=password).first()
        if user_login is not None:
            session['username'] = user_login.username
            session['id'] = user_login.id
            print(session['username'], session['id'])
            return redirect(url_for("viewpost"))
        else:
            print("Ensure a valid email/password is input!")
            render_template("login.html")
    return render_template("login.html")
