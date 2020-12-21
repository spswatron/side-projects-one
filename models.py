from sqlalchemy_searchable import make_searchable
from __init__ import db, app
from datetime import datetime
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
make_searchable(db.metadata)


class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'content']
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.UnicodeText, unique=True)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.UnicodeText, unique=True)
    content = db.Column(db.UnicodeText)
    image = db.Column(db.LargeBinary)
    show = db.Column(db.Boolean, default=False)

    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as connection:
        result = connection.execute("DROP FUNCTION IF EXISTS posts_search_vector_update() CASCADE")
    search_vector = db.Column(TSVectorType('title', 'content'))

    def __init__(self, url, title, content, image):
        self.url = url
        self.title = title
        self.content = content
        self.image = image

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'time': self.time,
            'title': self.title,
            'content': self.content,
            'show': self.show,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


db.configure_mappers()


class User(db.Model):
    __tablename__ = 'users'
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
