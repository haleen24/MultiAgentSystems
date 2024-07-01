from os import listdir
from os.path import join

from pm4py import read_pnml, write_pnml

if __name__ == "__main__":
    files = [join("test", i) for i in listdir("test")]
    # print(files)
    id = 0
    net_id = 1
    for i in files:
        net, marking, final = read_pnml(i)
        for j in net.transitions:
            j.label = str(id)
            id += 1
        net.name = f"Net {net_id}"
        net_id += 1
        write_pnml(net, marking, final, i)
