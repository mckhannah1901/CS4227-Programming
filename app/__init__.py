from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "cs4227"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_blog_post.db'
db = SQLAlchemy(app)

from app.models import Person, Blogpost, Comment
from app import addcomment, addpost, deletepost, editpost, login, logout, register, viewposts, routes
