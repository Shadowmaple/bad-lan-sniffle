# -*- coding: utf-8 -*-
from machine.DocEmbeddingBased.Sample_label import *
from machine.DocEmbeddingBased.Samples import (doc2vec_sample, sif_sample,
                                               tfidf_sample)
from machine.GraphBased.Samples import Graph_result
from machine.GraphBased.Samples_label import *
from machine.Utils.DataProcess import get_data_from_input


def use_doc2vec_sample(test:list):
    return doc2vec_sample(test)

def use_sif_sample(test:list):
    return sif_sample(test)

def use_tfidf_sample(test:list):
    return tfidf_sample(test)

def use_graph_sample(test:list):
    return Graph_result(test)

def classify(kind:int,docs:list):
    if kind == 0: return use_graph_sample(docs)
    elif kind == 1:return use_doc2vec_sample(docs)
    elif kind == 2:return use_sif_sample(docs)
    elif kind == 3:return use_tfidf_sample(docs)


def use_graph_label_sample(test:list):
    return Graph_result_label(test)


def use_tfidf_label_sample(test:list):
    return tfidf_label_sample(test)


def use_sif_label_sample(test:list):
    return sif_label_sample(test)


def use_doc2vec_label_sample(test:list):
    return doc2vec_label_sample(test)


def classify_label(kind:int,docs:list):
    docs = get_data_to_label(docs)
    if kind == 0:return use_graph_label_sample(docs)
    elif kind == 1:return use_doc2vec_label_sample(docs)
    elif kind == 2:return use_sif_label_sample(docs)
    elif kind == 3:return use_tfidf_label_sample(docs)


def get_data_to_label(docs:list):
    pairs = []
    for line in docs:
        items = line.split()
        pairs.append((items[0], "".join(items[1:])))

    return pairs


if __name__ == '__main__':
    docs:list
    kind = input("请输入您想要调用的分类器")
    kind = int(kind)

    docs = get_data_from_input()
    res = classify(kind,docs)

    for i in range(len(res)):
        print(res[i],docs[i])
