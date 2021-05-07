from flask import jsonify, request
from flask_cors import cross_origin

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
