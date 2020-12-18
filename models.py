from __init__ import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), unique=True)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(), unique=True)
    content = db.Column(db.String())
    show = db.Column(db.Boolean, default=False)

    def __init__(self, url, title, content):
        self.url = url
        self.title = title
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'time': self.time,
            'title': self.title,
            'content': self.content,
            'show': self.show
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active
