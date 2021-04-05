# -*- coding: utf-8 -*-
import os
import string

import jieba
import zhon.hanzi


# 统一工程中的停用词表获取方式
def __get_stopwords():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    # stopwords.txt 所在路径
    file_dir = os.path.join(project_dir, "Data/stopwords.txt")
    with open(file_dir, mode="r", encoding="utf8") as f:
        words = f.read().split()
    return words


# 判定是否为停用词
def __in_stopwords(word: str):
    return word in stopwords or word[0] in string.digits or word[0] in punctuations ## string.digits 是012 punctuations 是奇怪的标点符号


def get_data(file_name):
    """
    读取数据文件
    Parameters
    ----------
    file_name : str,
        数据文件路径，文件编码必须是utf-8，文件中每一行为（class_no， text）

    Returns
    -------
    pairs: list,
        每一项是tuple(class_no, text)
    """
    with open(file_name, mode="r", encoding="utf8") as file:
        lines = file.readlines()

    pairs = []
    for line in lines:
        items = line.split()
        pairs.append((items[0], "".join(items[1:])))

    return pairs


def format_data(data):
    """
    将数据按类别分开
    Parameters
    ----------
    data : list,
        每一项是(class_no, text)

    Returns
    -------
    classes: list,
        每一项是class_no
    texts_list: list,
        每一项是对应类别下的文本
    """
    texts_list = []
    classes = []
    for class_no, text in data:
        if class_no not in classes:
            classes.append(class_no)
            texts_list.append([])
        index = classes.index(class_no)
        texts_list[index].append(text)

    return classes, texts_list


def text_cut(text):
    """
    对文本进行逐句分词
    Parameters
    ----------
    text :  str,
        需要进行逐句分词的文本

    Returns
    -------
    sentences: list,
        每一项是list(str)代表分词后的一个句子
    """
    sentences = []
    sentence = []
    # text+"."是考虑到句子结尾可能没有标点
    for word in jieba.lcut(text + "."):
        if word in end_punctuations:
            sentences.append(sentence)
            sentence = []
        elif not __in_stopwords(word):
            sentence.append(word)
    return [x for x in sentences if x]


def tokenize(text, char_split=False, remove_stopwords=True):
    """
    文本分词
    Parameters
    ----------
    text : str,
        需要分词的文本
    char_split : bool (default = False)
        if True 则按字符切分，if False 则按词语切分
    remove_stopwords : bool (default = True)
        if True 则去除停用词，if False 则不去除停用词
    Returns
    -------
    tokens : list(str)
        分词结果
    """
    tokens = list(text) if char_split else list(jieba.lcut(text))
    return [token for token in tokens if not __in_stopwords(token)] if remove_stopwords else tokens


def get_data_from_input():
    """
    仿照get_data，但是功能是直接从input中输入数据
    :return:
    -------
    pairs: list,
        每一项是tuple(class_no, text)
    """
    n = input("请输入句子个数")
    n = int(n)
    lines = []
    for i in range(n):
        line = input("请输入句子")
        lines.append(line)

    pairs = []
    for line in lines:
        pairs.append(("".join(line[:])))

    return pairs

stopwords = __get_stopwords()
punctuations = string.punctuation + zhon.hanzi.punctuation
# 句末标点，会影响到TextGraph的生成
end_punctuations = list(",.;?!，。；？！…")

__all__ = ('get_data', 'format_data', 'text_cut', 'tokenize', 'stopwords','get_data_from_input')
