# -*- coding: utf-8 -*-
from machine.DocEmbeddingBased.DocEmbedding.ConverterBase import ConverterBase
from machine.Utils.DataProcess import tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class TFIDFConverter(ConverterBase):
    """
    用sklearn自带的TFDIF相关工具向量化文本
    """

    @classmethod
    def docs_to_vectors(cls, texts, custom_tokenize=None, stopwords=None):
        """
        将文本集合转化为对应的文本向量集
        Parameters
        ----------
        custom_tokenize : callable or None (default)
            分词器，若None则使用 Utils.DataProcess.tokenize(False, True)
        texts : list,
            每一项是str，代表需要向量化的文本
        stopwords : list or None (default)
            停用词表，若不需要去停用词则设为None
        Returns
        -------
        vectors : numpy.array(dim=2)
            得到的文本向量集合，每一项是一个 numpy.array(dim=1)类型的向量
        """
        if tokenize is not None:
            vectorizer = TfidfVectorizer(lowercase=False, tokenizer=custom_tokenize, stop_words=stopwords)
        else:
            vectorizer = TfidfVectorizer(lowercase=False, tokenizer=tokenize, stop_words=stopwords)
        X = vectorizer.fit_transform(texts)
        return X.toarray()
