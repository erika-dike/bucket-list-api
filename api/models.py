from datetime import datetime

from flask import current_app, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from errors import ValidationError

db = SQLAlchemy()

# date and time format
fmt = "%A, %d. %B %Y %I:%M%p"


class Base(db.Model):
    """Base model for the database"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, unique=True)

    # get time so date created and modified have same exact time
    now = datetime.now()

    date_created = db.Column(db.DateTime, default=now)
    date_modified = db.Column(db.DateTime, default=now,
                              onupdate=now)

    def save(self):
        """Saves instance object to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes instance object from database"""
        db.session.delete(self)
        db.session.commit()


class User(Base):
    """Users table"""

    __tablename__ = 'users'
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
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
        """"Verify authentication token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def get_url(self):
        """Get the url for this instance"""
        return url_for('api.get_user', id=self.id, _external=True)

    def to_json(self):
        """Packages instance as JSON object"""
        return {
            'url': self.get_url(),
            'name': self.username
        }


class BucketList(Base):
    """Bucket list table"""

    __tablename__ = 'bucketlist'
    name = db.Column(db.String(25), index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('BucketListItem', backref=db.backref(
        'bucketlist_item', lazy='joined'), cascade='all, delete-orphan',
        lazy='dynamic')

    def get_url(self):
        """Get the url for this instance"""
        return url_for('api.get_bucketlist', id=self.id, _external=True)

    @staticmethod
    def get_bucketlists_url():
        return url_for('api.get_bucketlists', _external=True)

    def to_json(self):
        """Packages instance as JSON object"""
        items = [item.to_json() for item in self.items]
        return {
            'id': self.id,
            'name': self.name,
            'items': items,
            'date_created': self.date_created.strftime(fmt),
            'date_modified': self.date_modified.strftime(fmt),
            'created_by': User.query.get(self.creator_id).username,
            'bucketlist_url': self.get_url()
        }

    def from_json(self, json):
        """Instantiates instance with data from JSON object"""
        try:
            self.name = json['name']
        except KeyError as e:
            raise ValidationError('Invalid name: missing ' + e.args[0])
        return self


class BucketListItem(Base):
    """Bucket list item table"""

    __tablename__ = 'bucketlist_item'
    name = db.Column(db.String(250), index=True)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def get_url(self):
        """Get the url for this intance"""
        return url_for('api.get_bucketlist_item',
                       id=self.bucketlist_id,
                       item_id=self.id,
                       _external=True)

    def to_json(self):
        """Packages instance as JSON object"""
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created.strftime(fmt),
            'date_modified': self.date_modified.strftime(fmt),
            'done': self.done,
            'item_url': self.get_url()
        }

    def from_json(self, json):
        """Instantiates instance with data from JSON object"""
        if 'done' in json:
            done = json['done'].lower()
            self.done = bool(1 if done == 'true' else 0)
        if 'name' in json:
            self.name = json['name']
        if not self.name:
            raise ValidationError(
                'Invalid argument {}. Allowed: [name] and/or [done]'.
                format(json.keys()))
        return self
