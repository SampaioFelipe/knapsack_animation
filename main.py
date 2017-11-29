from knapsack.greedy import *
from knapsack.definitions import *
from knapsack import drawer


def main():

    I = [Item(92, 23), Item(57, 31), Item(49, 29), Item(68, 44), Item(60, 53), Item(43, 38), Item(67, 63), Item(84, 85),
         Item(87, 89), Item(72, 82)]

    drawer.init_video_settings()

    greedy_knapsack(I, 165)

    while True:
        drawer.event_handler()
        drawer.draw()
        drawer.FPSCLOCK.tick(30)


if __name__ == '__main__':
    main()
