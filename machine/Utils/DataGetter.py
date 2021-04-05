# -*- coding: utf-8 -*-
import pandas as pd

from .DataProcess import get_data, get_data_from_input

# 数据见 https://github.com/SophonPlus/ChineseNlpCorpus
path_1 = "../Data/simplifyweibo_4_moods.csv"
path_2 = "../Data/waimai_10k.csv"
path_3 = "../Data/ChnSentiCorp_htl_all.csv"
path_4 = "../Data/weibo_senti_100k.csv"
# 参考数据 from 杨玉娟
path_data = "../Data/data.txt"
path_data02 = "./Data/data02.txt"
path_data03 = "../Data/data02.txt"

def get_balance_corpus(path, corpus_size):
    """
    从csv文件中获取平衡语料库
    Parameters
    ----------
    path : str,
        csv文件路径，格式要求：必须含有label列，另一列为对应的文本
    corpus_size : int,
        需要获取的语料库大小，采用随机采样方式，若文件中数据量小于需要的数据量则采用有放回抽样
    Returns
    -------
    data: list,
        每一项是(label, text): (int, str)
    """
    pd_all = pd.read_csv(path).astype(str)  ## 代码解释：astype 强制类型转换
    labels = set(pd_all["label"])
    sample_size = corpus_size // len(labels)
    samples = []
    for label in labels:
        tmp_corpus = pd_all[pd_all.label == label]
        sample = tmp_corpus.sample(sample_size, replace=tmp_corpus.shape[0] < sample_size)
        ### pandas.sample 用来取样 sample_size 用来规定获取的样例大小 replace代表是否放回抽样
        samples.append(sample)
    corpus_balance = pd.concat(samples)
    print(f"一共{len(corpus_balance)}条数据，分为{len(labels)}类，每类{sample_size}条")
    return [tuple(x) for x in corpus_balance.values]


__all__ = ('get_data', 'get_balance_corpus', 'path_1', 'path_2', 'path_3', 'path_4', 'path_data', 'path_data02','path_data03','get_data_from_input')
