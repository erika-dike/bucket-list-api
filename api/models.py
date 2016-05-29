from datetime import datetime

from flask import current_app, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    date_of_birth = db.Column(db.DateTime)
    bucketlist = db.relationship('BucketList', backref=db.backref(
        'bucketlist', lazy='joined'), cascade="all, delete-orphan",
        lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def to_json(self):
        return {
            'url': self.get_url,
            'name': self.name
        }


class BucketList(db.Model):
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('BucketListItem', backref=db.backref(
        'bucketlist_item', lazy='joined'), cascade='all, delete-orphan',
        lazy='dynamic')
    date_created = db.Column(db.DateTime)


class BucketListItem(db.Model):
    __tablename__ = 'bucketlist_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True)
    description = db.Column(db.Text, default="")
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
