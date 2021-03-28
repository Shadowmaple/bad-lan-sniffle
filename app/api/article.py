from . import api


@api.route('', methods = ['GET'])
def list():
    """
    获取新闻列表
    params:
      - page: 页码，从1开始
      - size: 数量
      - type: 板块类型，0/1/2/3
    """
    pass

@api.route('', methods = ['POST'])
def create():
    """
    创建新的新闻
    """
    pass

# @api.route('', methods = ['PUT'])
# def update():
#     pass

@api.route('', methods = ['DELETE'])
def delete():
    pass
