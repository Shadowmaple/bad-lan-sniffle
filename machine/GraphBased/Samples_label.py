from random import shuffle

from machine.GraphBased.Core.GraphKNN import GraphKnnClassifier
from machine.GraphBased.Utils.TextGraph import TextGraph
from machine.Utils.DataGetter import *
from machine.Utils.util import Get_trained_data_path
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def Graph_result_label(test:list):
    # data = get_data(path_data03)
    data = get_data(Get_trained_data_path())
    shuffle(data)
    ##print('部分数据展示：')
    ##for x in data[:5]:

    labels, graphs = [int(x[0]) for x in data], [TextGraph(x[1]) for x in data]
    train_graphs, test_graphs, train_labels, test_labels = train_test_split(graphs, labels, train_size=0.7,
                                                                            shuffle=True)
    classifier = GraphKnnClassifier(threshold=0.6, k=10, is_semi_supervised=False)

    classifier.fit(train_graphs, train_labels, test_graphs)

    ##print(len(data))
    test_graphs = [TextGraph(x[1]) for x in test]
    predicts = classifier.predict(test_graphs)

    final_result = predicts.tolist()
    ret = []

    for i in range(len(final_result)):
        tmp = {}
        tmp["content"] = test[i][1]
        tmp["origin"] = int(test[i][0])
        tmp["predict"] = int(final_result[i])
        ret.append(tmp)

    return ret
    ##print(type(final_result))

# if __name__ == '__main__':
#     docs:list
#     ##docs = get_data_from_input()
#     docs = get_data_from_label()
#     print(docs[0][1])
#     res = Graph_result_label(docs)

#     for i in range(len(res)):
#         print(res[i]["content"],res[i]["origin"],res[i]["predict"])
