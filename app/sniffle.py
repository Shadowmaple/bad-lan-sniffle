from machine.sample import classify


def Classify(kind:int, contents:list) -> list:
    """ 分类器 """
    if kind > 3 or kind < 0:
        return []

    data = classify(kind, contents)

    return data
