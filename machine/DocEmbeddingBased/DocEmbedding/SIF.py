# -*- coding: utf-8 -*-
from collections import Counter

import numpy as np
from gensim.models import Word2Vec
from gensim.models.keyedvectors import Word2VecKeyedVectors
from machine.DocEmbeddingBased.DocEmbedding.ConverterBase import ConverterBase
from machine.Utils.DataProcess import tokenize
from sklearn.decomposition import PCA


class Word2VecConfig:
    """
    配置类，参数意义请参考 gensim.models.Word2Vec
    """

    def __init__(self, size=300, window=5, min_count=5, sample=1e-3, workers=4, iter=5):
        self.size = size
        self.window = window
        self.min_count = min_count
        self.sample = sample
        self.workers = workers
        self.iter = iter


class SIFConverter(ConverterBase):
    """
    文本向量化工具，采用的 SIF方法可见会议论文：
        Sanjeev Arora, Yingyu Liang, Tengyu Ma.
        A Simple but Tough-to-Beat Baseline for Sentence Embeddings.
        In International Conference on Learning Representations, 2017.
    """

    @classmethod
    def tokens_to_vectors(
            cls, tokens_list, config: Word2VecConfig = None, a: float = 1e-3,
            w2v_model: Word2VecKeyedVectors = None):
        """
        将分词后的文本集合转化为对应的向量集合，需要注意的是tokens_list与w2v_model至少有一个不为None
        Parameters
        ----------
        config : Word2VecConfig or None (default)
            Word2Vec配置类，Word2Vec模型的部分参数配置，若既不传入Word2VecConfig也不传入w2v_model，那么将采用默认配置参数
        tokens_list : list
            分词后的文本集合，每一项是文本分词后的 token列表，所以实际上 tokens_list: list(list(str)))
        a : float (default = 1e-3)
            SIF方法的参数
        w2v_model : Word2VecKeyedVectors or None (default)
            不使用 tokens_list训练词向量模型而是直接加载已有的词向量模型
        Returns
        -------
        vectors : list
            训练得到的文本向量集合，每一项是一个 numpy.array类型的向量
        """
        config = config if config is not None else Word2VecConfig()
        model = w2v_model if w2v_model else Word2Vec(
            tokens_list,
            vector_size=config.size,
            window=config.window,
            min_count=config.min_count,
            sample=config.sample,
            workers=config.workers,
            # iter=config.iter
        )
        word_freq = cls.__calc_words_freq(tokens_list)
        vectors = [cls.__tokens_to_vector(s, word_freq, model, config.size, a) for s in tokens_list]
        vectors = cls.__vectors_pca(vectors, config.size)
        return vectors

    @classmethod
    def docs_to_vectors(cls, docs, config: Word2VecConfig = None, a: float = 1e-3,
                        w2v_model: Word2VecKeyedVectors = None,
                        char_split=False, remove_stopwords=True):
        """
        将文本集合转化为对应的文本向量集
        Parameters
        ----------
        docs : list
            文本集，每一项是一个纯文本
        config : Word2VecConfig or None (default)
            Word2Vec配置类，Word2Vec模型的部分参数配置，若既不传入Word2VecConfig也不传入w2v_model，那么将采用默认配置参数
        a : float (default = 1e-3)
            SIF方法的参数
        w2v_model : Word2VecKeyedVectors or None (default)
            不使用 tokens_list训练词向量模型而是直接加载已有的词向量模型
        char_split : bool (default = False)
            If True 采用字模型， If False 采用词模型
        remove_stopwords : bool (default = True)
            If True 去除停用词， If False 保留停用词
        Returns
        -------
        vectors : list
            训练得到的文本向量集合，每一项是一个 numpy.array类型的向量
        """
        tokens_list = [tokenize(doc, char_split=False, remove_stopwords=True) for doc in docs]
        return cls.tokens_to_vectors(tokens_list, config, a, w2v_model)

    @classmethod
    def __tokens_to_vector(cls, tokens: list, word_freq, model, embedding_size, a):
        """
        SIF的关键步骤一，组成文本向量
        Parameters
        ----------
        tokens : list,
            每一项是str代表一个词语，tokens由文本分词得到
        word_freq : dict,
            词频字典
        model : Word2VecKeyedVectors 或者 Word2Vec
            Word2Vec模型，用于得到词向量
        embedding_size : int,
            向量化的维度
        a : float,
            SIF的参数
        Returns
        -------
        vec : numpy.array,
            输入tokens对应的文本向量
        """
        if len(tokens) == 0:
            return np.ones(embedding_size)
        vec = np.zeros(embedding_size)
        # smooth inverse frequency, SIF
        for word in tokens:
            a_value = a / (a + word_freq[word])
            if word in model.wv:
                vec += a_value * model.wv[word]
        vec = vec / len(tokens)
        return vec

    @classmethod
    def __vectors_pca(cls, vectors, embedding_size):
        """
        SIF的关键步骤二，去除第一主成分方向上的投影
        Parameters
        ----------
        vectors : list,
            每一项是一个numpy.array类型的向量
        embedding_size : int,
            代表向量化的维度
        Returns
        -------
        vectors : list,
            每一项是一个numpy.array类型的向量，vectors是处理后的向量集
        """
        # calculate PCA of this sentence set
        pca = PCA()
        pca.fit(np.array(vectors))
        u = pca.components_[0]  # the PCA vector
        uT = u.reshape((len(u), 1))
        u = uT * u  # u x uT

        # pad the vector?  (occurs if we have less sentences than embeddings_size)
        if len(u) < embedding_size:
            for i in range(embedding_size - len(u)):
                u = np.append(u, 0)  # add needed extension for multiplication below

        # resulting sentence vectors, vs = vs -u x uT x vs
        vectors = [vec - np.matmul(u, vec) for vec in vectors]

        return vectors

    @classmethod
    def __calc_words_freq(cls, tokens_list):
        """
        计算词频表
        Parameters
        ----------
        tokens_list : list
            分词后的文本集合，每一项是文本分词后的 token列表，所以实际上 tokens_list: list(list(str)))
        Returns
        -------
        word_freq: dict
            key: str，代表词语； value: float，代表词频
        """
        counter = Counter()
        for tokens in tokens_list:
            counter.update(tokens)
        counts = sum(counter.values())
        word_freq = dict([(x[0], x[1] / counts) for x in counter.items()])
        return word_freq
