from knapsack.greedy import *
from knapsack.drawer import *
from knapsack.dynamicProgramming import *


def main():

    # I = [Item(57, 31), Item(49, 29), Item(68, 44), Item(60, 53), Item(43, 38), Item(67, 63), Item(84, 85),
    #      Item(87, 89), Item(72, 82), Item(92, 23)]
    #
    # i = 0
    #
    # for item in I:
    #     item.set_col(i)
    #     i = i + 1

    screen = Animation()
    screen.start()
    # screen.join()

    # print(greedy_knapsack(I, 165))
    # print(dynamicProgramming_knapsack(I, 165))

if __name__ == '__main__':
    main()
