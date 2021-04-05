# -*- coding: utf-8 -*-
from copy import deepcopy

import numpy as np
from machine.Utils.DataProcess import format_data
from sklearn.metrics import accuracy_score


class CentroidEM:
    """
    利用有标记样本取得几种类别的平均值特征值从而得到质心即Centroid，
    之后可根据是否利用无标记样本中的信息来使分类器运行于有监督或半监督模式，
    预测时衡量新样本与质心的距离并选取距离最小的质心对应的分类来作为预测值，
    本分类器衡量距离采用的是余弦距离，并且针对余弦距离已经做了分类器性能上的优化，
    模型用法类似sklearn，主要是fit，score，predict
    """

    # private variables: vector_size, classes, class_vectors, centroid_vectors
    def __init__(self, epsilon=1e-6, max_iter=1000):
        """
        Parameters
        ----------
        epsilon : float, (default = 1e-6)
            半监督学习停止条件之一，两次质心之差的二范数小于epsilon时停止迭代
        max_iter : int, (default = 1000)
            半监督学习停止条件之一，最大迭代次数，以防止训练时间过长
        """
        self.unlabeled_vectors = None
        self.norm_unlabeled_vectors = None
        self.vector_size = None
        self.classes = None
        self.class_vectors = None
        self.centroid_vectors = None
        self.norm_centroid_vectors = None
        self.epsilon = epsilon
        self.max_iter = max_iter

    def fit(self, labeled_vectors, labels, unlabeled_vectors=None):
        """
        训练模型，用法与
        Parameters
        ----------
        labeled_vectors : numpy.array(dim=2)
            已标记样本特征向量集
        labels : numpy.array(dim=1)
            已标记样本标签集
        unlabeled_vectors : numpy.array(dim=2) or None (default)
            未标记样本特征向量集，若不为None则代表分类器进行半监督学习，否则为有监督学习
        Returns
        -------
        无返回值
        """
        self.vector_size = labeled_vectors[0].shape[0]
        self.classes, self.class_vectors = format_data(zip(labels, labeled_vectors))
        self.centroid_vectors = [np.zeros(self.vector_size) for i in range(len(self.classes))]
        self.norm_centroid_vectors = [np.zeros(self.vector_size) for i in range(len(self.classes))]
        self.__update_centroid_vectors()
        if unlabeled_vectors is not None:
            self.unlabeled_vectors = unlabeled_vectors
            self.norm_unlabeled_vectors = [vec / np.linalg.norm(vec) for vec in unlabeled_vectors]
            self.__train()

    def score(self, test_vectors, test_labels):
        """
        评测分类器的精度
        Parameters
        ----------
        test_vectors : numpy.array(dim=2)
            测试样本特征向量集
        test_labels : numpy.array(dim=1)
            测试样本标签集
        Returns
        -------
        accuracy : float,
            测试样本集预测精度
        """
        predicts = self.predict(test_vectors)
        return accuracy_score(predicts, test_labels)

    def predict(self, vectors):
        """
        预测样本分类
        Parameters
        ----------
        vectors : numpy.array(dim=2),
            待预测样本特征向量集
        Returns
        -------
        predicts : numpy.array(dim=1),
            预测分类集
        """
        predicts = np.array([self.__predict_one(vec) for vec in vectors])
        return predicts

    # 预测一个样本的分类
    def __predict_one(self, vector):
        sims = np.array([x.dot(vector) for x in self.norm_centroid_vectors])
        index = np.argmax(sims)
        return self.classes[index]

    # 半监督学习训练的核心步骤，重复地对未标记样本进行预测并更新质心直到满足停止条件：
    # 质心变化不大或者达到最大迭代次数
    def __train(self):
        initial_class_vectors = deepcopy(self.class_vectors)
        error = self.epsilon + 1
        iter_count = 1
        while error > self.epsilon:
            if iter_count > self.max_iter:
                print(f"Training n_iter is greater than {self.max_iter} and training is finished.")
                break
            old_centroids = deepcopy(self.centroid_vectors)
            self.class_vectors = deepcopy(initial_class_vectors)
            self.__union_unlabeled_data()
            self.__update_centroid_vectors()
            new_centroids = self.centroid_vectors
            for i in range(len(self.classes)):
                error = np.linalg.norm(old_centroids[i] - new_centroids[i])
            iter_count += 1

    # 利用更新后的class_vectors中的信息更新质心
    def __update_centroid_vectors(self):
        """
        norm 是计算sqrt(x1^2 + x2^2 + .......)的一个函数
        """
        for i, vectors in enumerate(self.class_vectors):
            temp = np.zeros(self.vector_size)
            for vector in vectors:
                temp += vector
            self.centroid_vectors[i] = temp / len(vectors)
        self.norm_centroid_vectors = [x / np.linalg.norm(x) for x in self.centroid_vectors]

    # 利用当前的质心对所有未标记样本进行预测
    def __union_unlabeled_data(self):
        for norm_vector, vector in zip(self.norm_unlabeled_vectors, self.unlabeled_vectors):
            sims = np.array([x.dot(norm_vector) for x in self.norm_centroid_vectors])
            index = np.argmax(sims)
            self.class_vectors[index].append(vector)
