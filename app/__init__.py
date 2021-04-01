from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "cs4227"

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'cs4227.blog.website@gmail.com',
    "MAIL_PASSWORD": 'examplePassword5*'
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_blog_post.db'
app.config['TESTING'] = False
db = SQLAlchemy(app)
mail = Mail(app)

from app.models import Person, Blogpost, Comment
from app import add_comment, add_post, delete_post, edit_post, log_in, log_out, user_registration, viewposts, routes, \
    user_subscribing
