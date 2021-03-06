from flask import Flask, render_template, request, session
from sqlalchemy import create_engine
engine = create_engine('sqlite:///people.db')
connection = engine.raw_connection()
cursor = connection.cursor()


def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM person WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            message = 'Logged in successfully!'
            return render_template('index.html', message=message)
        else:
            message = 'Incorrect email/password!'
    return render_template('login.html', message=message)
