from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy

from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    date_of_birth = db.Column(db.DateTime)
    bucketlist = db.relationship('BucketList', backref=db.backref(
        'bucketlist', lazy='joined'), cascade="all, delete-orphan",
        lazy='dynamic')


class BucketList(db.Model):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(250), index=True)
    description = db.Column(db.Text, default="")
    date_created = db.Column(db.DateTime)
    date_last_modified = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
