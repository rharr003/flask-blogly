from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    image_url = db.Column(db.String(), default='none')

    posts = db.relationship('Post', cascade="all,delete", backref='user')


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class Tag(db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)


class PostTag(db.Model):

    __tablename__ = 'posttag'

    post_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, autoincrement=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, autoincrement=False)