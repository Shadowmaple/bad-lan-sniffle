# -*- coding: utf-8 -*-
import heapq
from copy import deepcopy  # ## copy 与 deepcopy 之间存在很大的区别

import numpy as np
from machine.GraphBased.Utils.TextGraph import TextGraph
from sklearn.metrics import accuracy_score  # ##导入的这个东西有什么用我也不知道，暂时先这样搞着


class GraphKnnClassifier:
    """
    基于GraphBased.Utils.TextGraph的文本分类器，核心是计算两个文本的相似度并提供给kNN分类器用于比较两个文本间的距离
    """

    def __init__(self, threshold=0.6, k=10, is_semi_supervised=False):
        """
        Parameters
        ----------
        threshold : float (default = 0.6)
            置信度阈值，在半监督学习过程中，预测未标记文本图类别时不仅需要该类相似度之和最大还需要这个相似度之和大于threshold
        k : int (default = 10)
            预测分类时k近邻分类中近邻个数
        is_semi_supervised : bool (default = False)
            代表是否开启半监督学习模式
        """
        self.__confidence_threshold = threshold
        self.__k = k
        self.__classify_graphs = None
        self.__classify_labels = None
        self.__is_semi_supervised = is_semi_supervised

    def fit(self, labeled_graphs: list, labels: list, unlabeled_graphs: list = None):
        """
        Parameters
        ----------
        labeled_graphs : list,
            有标记文本图列表
        labels : list,
            labeled_graphs对应的标记列表
        unlabeled_graphs : list or None (default)
            未标记文本图列表
        """
        self.__classify_graphs = deepcopy(labeled_graphs)
        self.__classify_labels = deepcopy(labels)
        if self.__is_semi_supervised is False:
            return
        # 半监督学习，当训练到某一轮后发现没有新的可以加入分类用的无标签文本图时训练结束
        unlabeled_indexes = list(range(len(unlabeled_graphs)))
        old_unlabeled_num = len(unlabeled_indexes) + 1
        while old_unlabeled_num > len(unlabeled_indexes):
            old_unlabeled_num = len(unlabeled_indexes)
            for i in unlabeled_indexes:
                predict = self.__predict_one(unlabeled_graphs[i])
                if predict[1] > self.__confidence_threshold:
                    self.__classify_graphs.append(unlabeled_graphs[i])
                    self.__classify_labels.append(predict[0])
                    unlabeled_indexes.remove(i)
        # print(f"classify_graphs_num={len(self.__classify_graphs)}")

    def score(self, test_graphs, test_labels):
        predicts = self.predict(test_graphs)
        return accuracy_score(predicts, test_labels)

    def predict(self, graphs):
        predicts = [self.__predict_one(g) for g in graphs]
        return np.array([p[0] for p in predicts])

    def __predict_one(self, graph):
        """
        Parameters
        ----------
        graph : TextGraph,
            待预测的文本图
        Returns
        -------
        (预测的类别, 该类别对应的置信度即相似度之和)
        """
        similarity = [
            (self.__classify_labels[i], TextGraph.calc_similarity(x, graph))
            for i, x in enumerate(self.__classify_graphs)
        ]
        knn = heapq.nlargest(self.__k, similarity, key=lambda x: x[1])
        class_dict = {}
        for nn in knn:
            if class_dict.__contains__(nn[0]):
                class_dict[nn[0]] += nn[1]
            else:
                class_dict[nn[0]] = nn[1]
        res = max(class_dict.items(), key=lambda x: x[1])
        return res

    def __str__(self):
        return f"Transformer=\"GraphText_kNN_Classifier\":\n" \
               f"k={self.__k}, Semi-Supervised={self.__is_semi_supervised}, threshold={self.__confidence_threshold}"

    def __repr__(self):
        return self.__str__()
