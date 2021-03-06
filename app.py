from flask import Flask, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
import re

from sqlalchemy import create_engine
engine = create_engine('sqlite:///people.db')
connection = engine.raw_connection()
cursor = connection.cursor()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'  # update this with a different URI???
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)


db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/')
def hello_world():
    return render_template('home-page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form \
            and 'email' in request.form and 'username' in request.form and 'password' in request.form:

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM person WHERE email = % s OR username = % s', (email, username, ))
        account = cursor.fetchall()
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
        elif not first_name or not last_name or not email or not username or not password:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO person VALUES (NULL, % s, % s, % s)', (first_name, last_name, email, username,
                                                                                 password, ))
            sqlalchemy.connection.commit()
            message = 'You have successfully registered! Welcome to the Blogging Engine!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
