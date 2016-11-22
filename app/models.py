from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# user role model
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship(
        'User',
        backref='role',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Role %r>' % self.name


# user model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id')
    )
    refresh_token = db.Column(db.String)
    sessions = db.relationship(
        'Session',
        backref='user',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# session model
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    date = db.Column(
        db.DateTime,
        default=datetime.utcnow()
    )

    def __repr__(self):
        return '<Session %r>' % self.id
