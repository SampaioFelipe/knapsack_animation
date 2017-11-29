from knapsack.greedy import *
from knapsack.drawer import *


def main():

    I = [Item(57, 31), Item(49, 29), Item(68, 44), Item(60, 53), Item(43, 38), Item(67, 63), Item(84, 85),
         Item(87, 89), Item(72, 82), Item(92, 23)]

    print(I)

    i = 0

    for item in I:
        item.set_col(i)
        i = i + 1

    screen = Animation(I, None)
    screen.start()

    greedy_knapsack(I, 165)

    screen.join()

if __name__ == '__main__':
    main()
