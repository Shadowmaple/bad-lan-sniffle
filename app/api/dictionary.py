from flask import jsonify, request
from flask_cors import cross_origin

from .. import db
from ..decorator import require_admin_login
from ..models import Dictionary
from . import api


@api.route('/dict', methods = ['GET'])
@cross_origin()
def List_dict():
    """
    获取不良语言词典
    params:
      - page: 页码，从1开始
      - size: 数量，默认为20
    """
    page = request.args.get("page") or "1"
    size = request.args.get("size") or "10"

    dictionaries = Dictionary.query.filter_by().paginate(page=int(page), per_page=int(size))
    list = []
    for item in dictionaries.items:
        list.append({
            'content': item.content
        })

    return jsonify({
            'msg': 'ok',
            'page': dictionaries.page,
            'pages': dictionaries.pages,
            'size': len(list),
            'list': list,
        }), 200


@api.route('/dict', methods=['POST'])
@require_admin_login
def Add_dict():
    """ 添加词典 """
    """
    {
        "list": [
            "...",
        ]
    }
    """
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
        article = Dictionary(content=item)
        db.session.add(article)

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200


@api.route('/dict', methods=['DELETE'])
@require_admin_login
def Remove_dict():
    """ 移除 """
    """
    {
        "list": [
            "..",
        ]
    }
    """
    body = request.get_json()
    if body is None:
        return jsonify({
            'msg': 'no data',
        }), 400

    list = body.get('list')
    for content in list:
        Dictionary.query.filter_by(content=content).delete()

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200
