from flask import jsonify, request

from .. import db
from ..models import Article
from . import api


@api.route('', methods = ['GET'])
def list():
    """
    获取新闻列表
    params:
    #   - page: 页码，从1开始
    #   - size: 数量
      - type: 板块类型，0/1/2/3
    """
    type = request.query_string("type")
    articles = Article.query.filter(type=type).all()

    list = []
    for article in articles:
        list.append(article)

    return jsonify({
            'msg': 'ok',
            'list': list,
        }), 200

@api.route('', methods = ['POST'])
def create():
    """
    创建新的新闻
    """
    body = request.get_json()
    # to do: check
    for item in body.list:
        article = Article(name=item.name, url=item.url, type=item.type)
        db.session.add(article)
    db.session.commit()

    return jsonify({'msg': 'ok'}), 200

@api.route('', methods = ['DELETE'])
def delete():
    body = request.get_json()

    if body is None:
        # to do
        db.session.delete()
    else:
        for id in body.list:
            article = Article.query.filter_by(id=id).first()
            db.session.delete(article)

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200
