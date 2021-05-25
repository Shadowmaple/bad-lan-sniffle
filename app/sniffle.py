from machine.sample import classify, classify_label


def Classify(kind:int, contents:list) -> list:
    """ 分类器 """
    if kind > 3 or kind < 0:
        return []

    data = classify(kind, contents)
    return data


def Classify_label(kind:int, contents:list)->list:
    if kind > 3 or kind < 0:
        return []
    data = classify_label(kind, contents)
    return data
