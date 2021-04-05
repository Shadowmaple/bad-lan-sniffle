# -*- coding: utf-8 -*-
from random import shuffle

from gensim.models import doc2vec
from machine.DocEmbeddingBased.DocEmbedding.ConverterBase import ConverterBase
from machine.Utils.DataProcess import tokenize


class Doc2VecConfig:
    """
    配置类，参数意义可见 gensim.models.doc2vec.Doc2Vec
    """

    def __init__(self, min_count=1, window=10, vector_size=300, worker=4, epochs=20, dm=1):
        self.min_count = min_count
        self.window = window
        self.vector_size = vector_size
        self.worker = worker
        self.epochs = epochs
        self.dm = dm


class Doc2VecConverter(ConverterBase):
    """
    将文本通过doc2vec方式向量化的工具类
    """

    @classmethod
    def __get_doc2vec_model(cls, train_corpus, config: Doc2VecConfig, train_epochs=20):
        """
        训练Doc2Vec模型
        Parameters
        ----------
        train_corpus : list
            训练用的语料库，每一项是 gensim.models.doc2vec.TaggedDocument
        config : Doc2VecConfig
            Doc2Vec模型的部分参数配置
        train_epochs : int (default = 20)
            为使训练更充分，在训练过程中会打乱语料库反复训练 train_epochs次
        Returns
        -------
        model: gensim.models.doc2vec.Doc2Vec
            训练得到的模型
        """
        model = doc2vec.Doc2Vec(
            min_count=config.min_count,
            window=config.window,
            vector_size=config.window,
            workers=config.worker,
            epochs=config.epochs,
            dm=config.dm
        )
        model.build_vocab(train_corpus)
        for epoch in range(train_epochs):
            shuffle(train_corpus)
            model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
        return model

    @classmethod
    def tokens_to_vectors(cls, tokens_list: list, config: Doc2VecConfig, train_epochs=20):
        """
        将分词后的文本集合转化为对应的向量集合
        Parameters
        ----------
        tokens_list : list
            分词后的文本集合，每一项是文本分词后的 token列表，所以实际上 tokens_list: list(list(str)))
        config : Doc2VecConfig
            Doc2Vec模型的部分参数配置
        train_epochs : int (default = 20)
            为使训练更充分，在训练过程中会打乱语料库反复训练 train_epochs次
        Returns
        -------
        vectors : list
            训练得到的文本向量集合，每一项是一个 numpy.array类型的向量
        """
        train_corpus = [
            doc2vec.TaggedDocument(tokens, [i]) for i, tokens in enumerate(tokens_list)
        ]

        model = cls.__get_doc2vec_model(train_corpus, config, train_epochs)
        vectors = [model.docvecs[i] for i in range(len(tokens_list))]

        return vectors

    @classmethod
    def docs_to_vectors(cls, docs, config: Doc2VecConfig, train_epochs=20, char_split=False, remove_stopwords=True):
        """
        将文本集合转化为对应的文本向量集
        Parameters
        ----------
        docs : list
            文本集，每一项是一个纯文本
        config : Doc2VecConfig
            Doc2Vec模型的部分参数配置
        train_epochs : int
            为使训练更充分，在训练过程中会打乱语料库反复训练 train_epochs次
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
        return cls.tokens_to_vectors(tokens_list, config, train_epochs)
