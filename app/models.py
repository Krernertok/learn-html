from . import db, login_manager
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .tagnames.tagnames import taglist
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = password
        db.session.add(self)
        return True

    def generate_email_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    definition = db.Column(db.String(256))

    @staticmethod
    def insert_tags():
        for key in taglist:
            tag = Tag(name=key, definition=taglist[key])
            db.session.add(tag)
        db.session.commit()

    @staticmethod
    def get_definition(name):
        tag = Tag.query.filter_by(name=name).first()
        if tag is None:
            return None
        else:
            return tag.definition

    @staticmethod
    def get_remaining_tags(tags):
        all_tags = Tag.query.all()
        remaining_tags = dict()
        for tag in all_tags:
            if tag.name not in tags:
                remaining_tags.update({tag.name: tag.definition})
        return remaining_tags


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_start = db.Column(db.DateTime, default=datetime.utcnow)
    right_answers = db.relationship('Tag', secondary='right_answers',
        backref=db.backref('sessions', lazy='dynamic'),
        lazy='dynamic')


right_answers = db.Table('right_answers',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.session_id')),
    db.Column('tag_name', db.String(64), db.ForeignKey('tags.name'))
)