from flask import Flask, render_template, request
import re


def register():
    message = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form \
            and 'email' in request.form and 'username' in request.form and 'password' in request.form:

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cursor = db.connection.cursor(SQLAlchemydb.cursors.DictCursor)
        cursor.execute('SELECT * FROM person WHERE email = % s OR username = % s', (email, username, ))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[A-Za-z]+', first_name):
            message = 'First name must contain only letters!'
        elif not re.match(r'[A-Za-z]+', last_name):
            message = 'Last name must contain only letters!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            message = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (first_name, last_name, email, username,
                                                                                 password, ))
            sqlalchemy.connection.commit()
            message = 'You have successfully registered! Welcome to the Blogging Engine!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)
