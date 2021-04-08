from flask import jsonify, request
from flask_cors import cross_origin

from .. import db
from ..decorator import require_admin_login
from ..models import Article
from . import api


@api.route('/article', methods=['GET'])
@cross_origin()
def List():
    """
    获取新闻列表
    params:
      - kind: 板块类型，0/1/2/3
    """
    kind = request.args.get("kind")
    if kind is None:
        return jsonify({
            'msg': 'kind is required',
        }), 400

    articles = Article.query.filter_by(kind=int(kind)).all()

    list = []
    for article in articles:
        item = {
            'id': article.id,
            'name': article.name,
            'url': article.url,
            'kind': article.kind,
            'date': article.date,
        }
        list.append(item)

    return jsonify({
        'msg': 'ok',
        'list': list,
    }), 200



@api.route('/article', methods=['POST'])
@require_admin_login
def Create():
    """ 创建文章 """
    body = request.get_json()
    if body is None:
        return jsonify({
            'msg': 'no data',
        }), 400
    list = body.get('list')
    if list is None or len(list) == 0:
        return jsonify({
            'msg': 'no data',
        }), 400

    for item in list:
        name = item.get('name')
        url = item.get('url')
        kind = item.get('kind')
        date = item.get('date')
        if name is None or url is None or kind is None or date is None:
            return jsonify({
            'msg': 'name, url, kind and date are required.',
        }), 400

        article = Article(name=name, url=url, kind=kind, date=date)
        db.session.add(article)

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200


@api.route('/article', methods=['DELETE'])
@require_admin_login
def Delete():
    """ 删除文章 """
    body = request.get_json()
    if body is None:
        return jsonify({
            'msg': 'no data',
        }), 400

    list = body.get('list')
    kind = body.get('kind')
    # 无数据则默认全部删除
    if list is None or len(list) == 0:
        articles = []
        if kind is not None:
            articles = Article.query.filter_by(kind=int(kind)).all()
        else:
            articles = Article.query.all()

        for article in articles:
            db.session.delete(article)
    else:
        for id in list:
            article = Article.query.filter_by(id=id).first()
            db.session.delete(article)

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200
