from app import db
from app.models import Dictionary


def insertBadDict():
    lans = ['傻逼', '曹尼玛', '狗东西', '脑残', '']
    for item in lans:
        dic = Dictionary(content=item, count=1)
        db.session.add(dic)

    db.session.commit()
