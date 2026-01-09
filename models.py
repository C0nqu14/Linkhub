from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import url_for

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200), default=None)
    role = db.Column(db.String(10), default='user')
    karma = db.Column(db.Integer, default=0)
    posts = db.relationship('AppPost', backref='author', lazy=True, cascade="all, delete-orphan")
    
    def get_avatar(self):
        if self.avatar:
            return url_for('static', filename='uploads/avatars/' + self.avatar)
        return f"https://ui-avatars.com/api/?name={self.username}&background=random&color=fff"

class AppPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500))
    version = db.Column(db.String(20))
    description = db.Column(db.Text)
    download_url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending') 
    votes = db.Column(db.Integer, default=0)
    reports = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('app_post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user = db.relationship('User', backref='user_comments')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('app_post.id'))
    value = db.Column(db.Integer) 

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))