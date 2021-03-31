import chardet
from flask import jsonify, request

from . import api

# from werkzeug.utils import secure_filename

# 换行符
WIN_END = "\r\n" # windows
UNIX_END = "\n" # Unix/Linux
CONTENT_TYPE_FORM_DATA = 'multipart/form-data'
CONTENT_TYPE_JSON = 'application/json'

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@api.route('/sniffle', methods = ['POST'])
def sniffle():
    """ 不良语言检测 """
    # upload_file = request.files['file']
    # if upload_file and allowed_file(upload_file.filename):
    #     filename = secure_filename(upload_file.filename)
        # upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

    # print(request.files)

    content_type = request.headers['Content-Type']
    print(content_type)

    list = []
    if content_type.find(CONTENT_TYPE_FORM_DATA) != -1:
        file = request.files.get('file') # 类型：<class 'werkzeug.datastructures.FileStorage'>
        if file is None:
            return jsonify({
                    'msg': 'no file',
                }), 400
        list = handle_file_content(file=file)
    elif content_type.find(CONTENT_TYPE_JSON) != -1:
        data = request.json.get('data')
        if data is None:
            return jsonify({
                    'msg': 'no data',
                }), 400
        list = data
    else:
        return jsonify({
                'msg': 'no content-type',
            }), 400

    print(list)
    if len(list) == 0:
        return jsonify({
                'msg': 'no content',
                'list': {},
            }), 200

    # 不良语言分类器检测
    # ...

    return jsonify({
            'msg': 'ok',
            'list': '',
        }), 200


def handle_file_content(file, os='unix'):
    """ 处理文件内容 """
    # file_content = file.stream.read()
    file_content = file.read()

    # 编码统一为 utf-8
    encoding = chardet.detect(file_content)['encoding']
    if encoding != 'utf-8':
        file_content = file_content.decode(encoding).encode('utf-8')
    print(file_content)

    # bytes 类型转为 str
    content = str(file_content, encoding='utf-8')
    # Win下换行符是 \r\n，统一成 Unix 下的 \n
    if content.find(WIN_END) != -1:
        content = content.replace(WIN_END, UNIX_END)

    # 以换行符分割，并去除末尾的空串
    list = content.split(UNIX_END)
    if list.count('') > 0:
        list = list[:list.index('')]

    return list