from enum import unique

from app.sniffle import Classify

from . import db


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, index=False)
    url = db.Column(db.String(255), unique=False, index=False)
    kind = db.Column(db.Integer, unique=False, index=False) # 板块类别，0/1/2/3
    date = db.Column(db.String(15), unique=False, index=False) # 文章发布日期


# 不良语言词典
class Dictionary(db.Model):
    __tablename__ = "dictionary"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), unique=False, index=False) # 不良语言文本内容
    count = db.Column(db.Integer, unique=False, index=False) # 计数，暂时用不到


def NewDictionaryRecords(contents:list):
    """ 判定语句串，若所有分类器判定结果为不良语言，则加入词典中 """
    size = len(contents)
    result = [0]*size
    # kind = [0,3]
    for kind in range(4):
        data = Classify(kind=kind, contents=contents)
        result = [result[i] + data[i] for i in range(size)]

    for i in range(size):
        if result[i] != 0:
            continue
        # 所有分类器都判定它是不良语言，则将其加入词典中
        temp = Dictionary.query.filter_by(content=contents[i]).first()
        if temp is not None:
            continue
        item = Dictionary(content=contents[i], count=1)
        db.session.add(item)

    db.session.commit()
