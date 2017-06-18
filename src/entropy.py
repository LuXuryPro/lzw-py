import argparse
from collections import Counter

import math

args = argparse.ArgumentParser()
args.add_argument("-s", help="information source block size", type=int, default=1)
args.add_argument("-g", help="draw hitsogram", action="store_true", default=False)
args.add_argument("file", help="File to examin")
p = args.parse_args()

f = open(p.file, "rb")

bytes = list(f.read())
bcopy = list(bytes)
all = []

while bcopy:
    wo = ""
    for i in range(1):
        if not bytes:
            break
        wo += str(bcopy.pop())
    all.append(wo)

lns = len(all)

counter = Counter(all)
print(str.format('{0:.6f}',-sum( (count/lns) * math.log(count/lns, 2) for count in counter.values())))

if p.g:
    import matplotlib.pyplot as plt
    import numpy as np

    labels, values = zip(*sorted(list(counter.items()), key=lambda x: int(x[0])))

    indexes = np.arange(len(labels))
    width = 1
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

bcopy = list(bytes)
all = []

while bcopy:
    wo = ""
    for i in range(2):
        if not bcopy:
            break
        wo += str(bcopy.pop())
    all.append(wo)

lns = len(all)

counter = Counter(all)
print(str.format('{0:.6f}',-sum( (count/lns) * math.log(count/lns, 2) for count in counter.values()) / 2))

bcopy = list(bytes)
all = []

while bcopy:
    wo = ""
    for i in range(3):
        if not bcopy:
            break
        wo += str(bcopy.pop())
    all.append(wo)

lns = len(all)

counter = Counter(all)
print(str.format('{0:.6f}', -sum( (count/lns) * math.log(count/lns, 2) for count in counter.values()) / 3))

