from flask import request, render_template, redirect, url_for

from app import app, Person, db


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        registration = Person(first_name=first_name, last_name=last_name,
                              email=email, username=username, password=password)

        unique_email = db.session.query(Person.id).filter_by(email=email).first()
        unique_username = db.session.query(Person.id).filter_by(username=username).first()

        if first_name == '' or last_name == '' or email == '' or username == '' or password == '':
            print("All fields of the form must be filled in!")
            render_template("register.html")
        elif unique_email:
            print("This email already exists in the database. Please choose another!")
            render_template("register.html")
        elif unique_username:
            print("This username already exists in the database. Please choose another!")
            render_template("register.html")
        else:
            db.session.add(registration)
            db.session.commit()
            print("Registration completed successfully!")
            return redirect(url_for("login"))

    return render_template("register.html")
