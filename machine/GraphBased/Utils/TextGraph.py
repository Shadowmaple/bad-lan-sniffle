# -*- coding: utf-8 -*-
from collections import Counter

from machine.Utils.DataProcess import text_cut


class TextGraph:
    """
    文本的有向图表示，采用邻接矩阵，self.weights[a][b]表示的是(vertex_a, vertex_b)的相关程度，具体地，
            weights[a][b] = freq(word_a, word_b) / (2 * freq(word_a) * freq(word_b) - freq(word_a, word_b))
    """

    def __init__(self, text, theta=0.5, n_characters=10):
        """
        Parameters
        ----------
        text : str
            文本图所表示的文本
        theta : float (default = 0.5)
            相似度计算公式中的参数，最大公共子图项所占比例
        n_characters :int (default = 10)
            文本图中最多含有n_characters个结点，此处筛掉词频较低的词语
        """
        self.theta = theta
        self.character_num = n_characters
        self.sentences = text_cut(text)
        self.word_dict = self.__calc_word_dict()
        self.__character_filter()
        self.weights = self.__calc_edges()
        self.__del_nodes_isolate()
        self.weights = self.__calc_weights()

    # 修饰符解释：加入classmethod后，对应的函数不需要实例化，不需要self参数，但是第一个参数
    # 需要是表示自身类的cls参数，可以用来调用类的属性，类的方法，类的实例化对象等
    @classmethod
    def calc_similarity(cls, self, other):
        """
        计算相似度时考虑最大公共子图与公共边，具体地，
            sims_mcs = n_nodes(mcs(graph_a, graph_b)) / (1 + max(n_nodes(graph_a), n_nodes(graph_b)))
            sims_edge = Sigma_公共边{min(weight_a,weight_b)/max(weight_a,weight_b)} / (1 + 公共边个数)
            sims(graph_a, graph_b) = theta * sims_mcs + (1 - theta) * sims_edge
        Parameters
        ----------
        self :
        other :

        Returns
        -------
            sims: float, 两文本图的相似度
        """
        # print(self.__text + " " + other.__text)
        mcs_nodes, mcs_edges = TextGraph.max_common_subgraph(self, other)
        item_1 = len(mcs_nodes) / (1 + max(len(self.word_dict), len(other.word_dict)))
        item_2 = 0
        for edge in mcs_edges:
            for pair in edge:
                if pair:
                    item_2 += min(pair[0], pair[1]) / max(pair[0], pair[1])
        item_2 = item_2 / (1 + max(self.calc_edges_num(), other.calc_edges_num()))
        return self.theta * item_1 + (1 - self.theta) * item_2

    @classmethod
    def max_common_subgraph(cls, self, other):
        """
        暴力枚举寻找两个文本图的最大公共子图 mcs：
        第一步，列出两图之间的公共结点 mcs_nodes并建立初始化 mcs的邻接矩阵为零矩阵
        第二步，遍历两图邻接矩阵中公共结点对应的边 edge_1、edge_2，
            若都不为0，则认为 mcs也含有该边，修改对应矩阵项为 (weight_1, weight_2)以便后用
        Parameters
        ----------
        self :
        other :

        Returns
        -------
            mcs_nodes: list(str), 最大公共子图的结点对应的词列表,
            mcs_edges: 二级列表,可以简单看成是最大公共子图的邻接矩阵，只是存在边的对应项是(weight_1, weight_2)，
                其中 weight_1、weight_2分别代表两图公共边邻接矩阵中对应的权值
        """
        nodes_1 = list(self.word_dict.keys())
        nodes_2 = list(other.word_dict.keys())
        mcs_nodes = [x for x in nodes_1 if x in nodes_2]
        mcs_nodes_num = len(mcs_nodes)
        mcs_nodes_index_1 = [nodes_1.index(x) for x in mcs_nodes]
        mcs_nodes_index_2 = [nodes_2.index(x) for x in mcs_nodes]
        mcs_edges = [[0 for j in range(mcs_nodes_num)] for i in range(mcs_nodes_num)]
        for i in range(mcs_nodes_num):
            for j in range(mcs_nodes_num):
                (x_1, y_1) = (mcs_nodes_index_1[i], mcs_nodes_index_1[j])
                (x_2, y_2) = (mcs_nodes_index_2[i], mcs_nodes_index_2[j])
                if self.weights[x_1][y_1] and other.weights[x_2][y_2]:
                    mcs_edges[i][j] = (self.weights[x_1][y_1], other.weights[x_2][y_2])
        return mcs_nodes, mcs_edges

    # 统计词频
    def __calc_word_dict(self):
        counter = Counter()
        for sentence in self.sentences:
            counter.update(sentence)
        return counter

    # 特征选择，采用最简单的策略：选择词频最高的character_num个
    # 并且更新了 __word_dict, __sentences
    def __character_filter(self):
        if len(self.word_dict) > self.character_num:
            self.word_dict = dict(self.word_dict.most_common(self.character_num))
            for i in range(len(self.sentences)):
                self.sentences[i] = [x for x in self.sentences[i] if self.word_dict.__contains__(x)]
            self.sentences = [x for x in self.sentences if x]

    # 连接出现于同一句子的词对应的有向边（即修改__weights对应位置为1）
    def __calc_edges(self):
        words = list(self.word_dict.keys())
        word_index_dict = dict([(word, i) for i, word in enumerate(words)])
        weights = [[0 for i in range(len(words))] for j in range(len(words))]
        for sentence in self.sentences:
            for i in range(0, len(sentence) - 1):
                for j in range(i + 1, len(sentence)):
                    (x, y) = (word_index_dict[sentence[i]], word_index_dict[sentence[j]])
                    weights[x][y] = 1
        return weights

    # 删除孤立结点，并且更新 __word_dict, __sentences, __weights
    def __del_nodes_isolate(self):
        # 先找出非孤立的结点，并将信息存入两个joined开头的列表
        words = list(self.word_dict.keys())
        words_num = len(self.weights)
        signs = [0 for i in range(words_num)]
        for i in range(words_num):
            for j in range(words_num):
                if self.weights[i][j]:
                    signs[i] = 1
                    signs[j] = 1
        joined_nodes = [i for i in range(len(signs)) if signs[i]]
        joined_words = [words[i] for i in joined_nodes]
        # 删除孤立结点信息
        self.word_dict = dict([x for x in self.word_dict.items() if x[0] in joined_words])
        self.weights = [[self.weights[i][j] for j in joined_nodes] for i in joined_nodes]
        for i in range(len(self.sentences)):
            self.sentences[i] = [x for x in self.sentences[i] if x in joined_words]
        self.sentences = [x for x in self.sentences if x]

    # 计算边的权重矩阵
    def __calc_weights(self):
        words = list(self.word_dict.keys())
        loop = len(self.weights)
        return [
            [self.__calc_weights_word12(words[i], words[j]) for j in range(loop)] for i in range(loop)
        ]

    # 计算word_1, word_2对应边的权重
    def __calc_weights_word12(self, word_1, word_2):
        # 计算 freq(word_1, word_2)
        freq12 = 0
        for sentence in self.sentences:
            for i in range(0, len(sentence) - 1):
                for j in range(i + 1, len(sentence)):
                    if sentence[i] == word_1 and sentence[j] == word_2:
                        freq12 += 1
        # print("%s: %s, %s: %s, freq12=%s"%(word_1, self.__word_dict[word_1], word_2, self.__word_dict[word_2], str(freq12)))
        ratio = freq12 / (2 * self.word_dict[word_1] * self.word_dict[word_2] - freq12)
        return ratio
        # return math.log(1 + ratio)

    # 计算图中有向边的个数
    def calc_edges_num(self):
        count = 0
        for weight_vec in self.weights:
            for weight in weight_vec:
                if weight:
                    count += 1
        return count
