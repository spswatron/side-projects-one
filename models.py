from app import db
from sqlalchemy.dialects.postgresql import JSON


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)