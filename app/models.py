from . import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=False, index=False)
    url = db.Column(db.String(255), unique=False, index=False)
