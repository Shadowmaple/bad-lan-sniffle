from flask import jsonify, request
from flask_cors import cross_origin

from ..sniffle import Classify_label
from . import api

# 换行符
WIN_END = "\r\n" # windows
UNIX_END = "\n" # Unix/Linux

@api.route('/sniffle2', methods = ['POST'])
@cross_origin()
def sniffle2():
    """
    不良语言检测，带预测标签
    params:
    - kind：分类器类别，0/1/2/3
    """
    list = []
    data = request.json.get('data')
    if data is None or len(data) == 0:
        return jsonify({
                'msg': 'no data',
            }), 400
    for item in data:
        content = item.get('content')
        if content.find("\n") == -1:
            list.append(content)
        else:
            contents = split_content(content=content)
            list.extend(contents)

    kind = request.args.get("kind")
    if kind is None:
        kind = 0

    # 不良语言分类器检测
    classify_res = Classify_label(kind=int(kind), contents=list)

    data = []
    for i in range(len(classify_res)):
        data.append({
            "content": list[i],
            "result": classify_res[i],
        })

    return jsonify({
            'msg': 'ok',
            'data': data,
        }), 200


def split_content(content:str):
    # Win下换行符是 \r\n，统一成 Unix 下的 \n
    if content.find(WIN_END) != -1:
        content = content.replace(WIN_END, UNIX_END)

    # 以换行符分割，并去除末尾的空串
    list = content.split(UNIX_END)
    if list.count('') > 0:
        list = list[:list.index('')]

    return list
