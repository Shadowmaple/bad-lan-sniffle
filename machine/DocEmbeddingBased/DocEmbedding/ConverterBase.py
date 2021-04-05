# -*- coding: utf-8 -*-

class ConverterBase:
    @classmethod
    def docs_to_vectors(cls, docs, embedding_size):
        raise NotImplementedError()
