import argparse
from collections import Counter

import math

args = argparse.ArgumentParser()
args.add_argument("-s", help="information source block size", type=int, default=1)
args.add_argument("file", help="File to examin")
p = args.parse_args()

f = open(p.file, "rb")

bytes = list(f.read())

all = []

while bytes:
    wo = ""
    for i in range(p.s):
        if not bytes:
            break
        wo += str(bytes.pop())
    all.append(wo)

p, lns = Counter(all), float(len(all))
print(-sum( count/lns * math.log(count/lns, 2) for count in p.values()))

import matplotlib.pyplot as plt
import numpy as np

labels, values = zip(*p.items())

indexes = np.arange(len(labels))
width = 1
plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5, labels)
plt.show()