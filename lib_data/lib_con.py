
def readData():
    path = "./data02.txt"
    f = open(path, "r", encoding="utf-8")

    res = []

    lines = f.readlines()
    f.close()
    for line in lines:
        x = line.split(" ")
        if len(x) < 2:
            print("err", line)
    #    print(x[1])
        res.append(x[1].split("\n")[0])

    # with open("./lib_origin.txt", "w", encoding="utf-8") as f1:
    #     # f1.write(print(res))
    #     s = ",".join(res)
    #     print(s)

    # python3 lib_con.py > lib_origin.txt
    print(res)


def replace():
    f = open("./lib_origin.txt", "r", encoding="utf-8")
    line = f.readline()
    f.close()
    # print(line)
    a = line.replace("'", '"')
    a = a.replace('""', '"')
    with open("./lib_tar.txt", "w", encoding="utf-8") as f2:
        f2.write(a)


if __name__ == "__main__":
    # readData()
    replace()
