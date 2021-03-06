from flask import Flask, render_template, request, session


def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        email = request.form['email']
        password = request.form['password']

        cursor = db.connection.cursor(SQLAlchemydb.cursors.DictCursor)
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
