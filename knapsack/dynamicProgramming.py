import sys

from knapsack.definitions import DELAY
import time


def dynamicProgramming_knapsack(itens, k, c, control):

    for i in range(len(itens) + 1):
        for p in range(c + 1):

            if control.is_set():
                sys.exit(0)

            if i == 0 or p == 0:
                k[i][p] = 0
            elif itens[i - 1].peso <= p:
                k[i][p] = max(itens[i - 1].valor + k[i - 1][p - itens[i - 1].peso], k[i - 1][p])

            else:
                k[i][p] = k[i - 1][p]

            time.sleep(DELAY)

    return k
