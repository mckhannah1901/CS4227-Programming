from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'  # update this with a different URI???
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/')
def hello_world():
    return render_template('home-page.html')


if __name__ == '__main__':
    app.run()
