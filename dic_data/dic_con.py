
def readData():
    path1 = "./dic_bk.txt"
    path2 = "./dic_fd.txt"
    path3 = "./dic_wf.txt"
    f = open(path1, "r", encoding="utf-8")

    res = []

    lines = f.readlines()
    f.close()
    for line in lines:
        res.append(line.split("\n")[0])

    f = open(path2, "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    for line in lines:
        res.append(line.split("\n")[0])

    f = open(path3, "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    for line in lines:
        res.append(line.split("\n")[0])

    res.sort(reverse=True)

    # python3 dic_con.py > dic_origin.txt
    print(res)


def replace():
    f = open("./dic_origin.txt", "r", encoding="utf-8")
    line = f.readline()
    f.close()
    a = line.replace("'", '"')
    a = a.replace('""', '"')
    with open("./dic_tar.txt", "w", encoding="utf-8") as f2:
        f2.write(a)


if __name__ == "__main__":
    # readData()
    replace()
