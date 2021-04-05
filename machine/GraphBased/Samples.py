# -*- coding: utf-8 -*-
import os
from random import shuffle

from machine.GraphBased.Core.GraphKNN import GraphKnnClassifier
from machine.GraphBased.Utils.TextGraph import TextGraph
from machine.Utils.DataGetter import *
from machine.Utils.util import Get_trained_data_path
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def Graph_result(test:list):
    data = get_data(Get_trained_data_path())
    # data = get_data("/Data/data02.txt")
    # data = get_data(path_data03)
    shuffle(data)

    labels, graphs = [int(x[0]) for x in data], [TextGraph(x[1]) for x in data]
    train_graphs, test_graphs, train_labels, test_labels = train_test_split(graphs, labels, train_size=0.7,
                                                                            shuffle=True)
    classifier = GraphKnnClassifier(threshold=0.6, k=10, is_semi_supervised=False)

    classifier.fit(train_graphs, train_labels, test_graphs)

    ##print(len(data))
    test_graphs = [TextGraph(x) for x in test]
    predicts = classifier.predict(test_graphs)

    final_result = predicts.tolist()
    return final_result

if __name__ == '__main__':
    docs:list
    docs = get_data_from_input()
    res = Graph_result(docs)

    for i in range(len(res)):
        print(res[i],docs[i])
