import random

from machine.DocEmbeddingBased.CentroidEM import CentroidEM
from machine.DocEmbeddingBased.DocEmbedding.Doc2Vec import (Doc2VecConfig,
                                                            Doc2VecConverter)
from machine.DocEmbeddingBased.DocEmbedding.SIF import (SIFConverter,
                                                        Word2VecConfig)
from machine.DocEmbeddingBased.DocEmbedding.TFIDF import TFIDFConverter
from machine.Utils.DataGetter import get_data, get_data_from_input, path_data03
from machine.Utils.DataProcess import stopwords
from machine.Utils.util import Get_trained_data_path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def doc2vec_sample(test:list):
    if(len(test) == 0): return []

    data = get_data(Get_trained_data_path())
    # data = get_data("./Data/data02.txt")
    # data = get_data(path_data03)
    random.shuffle(data)
    docs = [x[1] for x in data]
    labels = [int(x[0]) for x in data]
    config = Doc2VecConfig(
        min_count=1, window=5, vector_size=300, worker=4, epochs=10, dm=1
    )
    arrays = Doc2VecConverter.docs_to_vectors(
        docs=docs, config=config, train_epochs=10, char_split=False, remove_stopwords=True
    )
    train_x, test_x, train_y, test_y = train_test_split(arrays, labels, train_size=0.7, shuffle=True)

    classifier = CentroidEM(epsilon=0.001, max_iter=100)
    classifier.fit(train_x, train_y, None)

    test = Doc2VecConverter.docs_to_vectors(
        docs=test, config=config, train_epochs=10, char_split=False, remove_stopwords=True
    )

    test = classifier.predict(test)

    test = test.tolist()
    ##print(type(test))

    ##for i in range(len(article)):
    ##    print(test[i],article)
    return test
    ## report = classification_report(y_true=test_y, y_pred=classifier.predict(test_x))
    ## print(report)


def sif_sample(test:list):
    # data = get_data(path_data03)
    # data = get_data("./Data/data02.txt")
    data = get_data(Get_trained_data_path())
    random.shuffle(data)
    docs = [x[1] for x in data]
    labels = [int(x[0]) for x in data]
    """
    读取信息
    注意这里输入的样例至少要为两个
    """
    for i in range(len(test)):
        docs.append(test[i])
    for i in range(len(test)):
        labels.append(0)

    config = Word2VecConfig(size=300, window=5, min_count=1, sample=0.1, workers=4, iter=5)
    arrays = SIFConverter.docs_to_vectors(
        docs=docs, config=config, a=1e-3, w2v_model=None, remove_stopwords=True, char_split=False
    )
    train_x, test_x, train_y, test_y = train_test_split(arrays, labels, train_size=1000, shuffle=False)
    classifier = CentroidEM(epsilon=1e-4, max_iter=100)
    classifier.fit(train_x, train_y, None)


    test = classifier.predict(test_x)
    test = test.tolist()

    ##for i in range(len(article)):
    ##    print(test[i],article)

    return test
    ## report = classification_report(y_true=test_y, y_pred=classifier.predict(test_x))
    ## print(report)


def tfidf_sample(test:list):
    data = get_data(Get_trained_data_path())
    # data = get_data(path_data03)
    random.shuffle(data)
    docs = [x[1] for x in data]
    labels = [int(x[0]) for x in data]
    """
    读取信息
    """
    for i in range(len(test)):
        docs.append(test[i])
    for i in range(len(test)):
        labels.append(0)

    arrays = TFIDFConverter.docs_to_vectors(texts=docs, stopwords=stopwords, custom_tokenize=None)
    train_x, test_x, train_y, test_y = train_test_split(arrays, labels, train_size=1000, shuffle=False)
    classifier = LogisticRegression(solver="liblinear", multi_class="auto")
    classifier.fit(train_x, train_y)

    test = classifier.predict(test_x)
    test = test.tolist()
    ## print(len(test))
    ##for i in range(len(article)):
    ##    print(test[i],article)
    return test
    ##report = classification_report(y_true=test_y, y_pred=classifier.predict(test_x))
    ##print(report)


if __name__ == '__main__':
    pass
    docs:list
    docs = get_data_from_input()

    ## res = doc2vec_sample(docs)
    ## res = sif_sample(docs)
    ## res = tfidf_sample(docs)
    ##for i in range(len(res)):
    ##    print(res[i],docs[i])
