from flask import jsonify, request
from flask_cors import cross_origin

from .. import db
from ..decorator import require_admin_login
from ..models import Dictionary
from . import api


@api.route('/dict', methods=['POST'])
@require_admin_login
def Add_dic():
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
def Remove():
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
