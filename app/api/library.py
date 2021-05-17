from flask import jsonify, request
from flask_cors import cross_origin

from .. import db
from ..decorator import require_admin_login
from ..models import Library
from . import api


@api.route('/lib', methods = ['GET'])
@cross_origin()
def List_lib():
    """
    获取不良语料库
    params:
      - page: 页码，从1开始
      - size: 数量，默认为20
    """
    page = request.args.get("page") or "1"
    size = request.args.get("size") or "10"

    library = Library.query.filter_by().paginate(page=int(page), per_page=int(size))
    list = []
    for item in library.items:
        list.append({
            'content': item.content
        })

    return jsonify({
            'msg': 'ok',
            'page': library.page,
            'pages': library.pages,
            'size': len(list),
            'list': list,
        }), 200


@api.route('/lib', methods=['POST'])
@require_admin_login
def Add_dic():
    """ 添加语料库 """
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
        lib = Library(content=item, count=1)
        db.session.add(lib)

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200


@api.route('/lib', methods=['DELETE'])
@require_admin_login
def Remove_lib():
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
        Library.query.filter_by(content=content).delete()

    db.session.commit()

    return jsonify({'msg': 'ok'}), 200
