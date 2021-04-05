import os


def Get_path()->str:
    """ 获取当前项目绝对路径 """
    return os.getcwd()

def Get_trained_data_path()->str:
    """ 获取训练数据文件路径 """
    return Get_path() + "/machine" + "/Data/data02.txt"
