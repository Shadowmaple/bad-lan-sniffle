from enum import unique

from . import db


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, index=False)
    url = db.Column(db.String(255), unique=False, index=False)
    type = db.Column(db.Integer, unique=False, index=False) # 板块类别，0/1/2/3
