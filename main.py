import sys
import traceback
from knapsack.drawer import Animation, pygame


def main():
    screen = Animation()
    screen.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        tb = sys.exc_info()[2]

        traceback.print_exception(e.__class__, e, tb)
        pygame.quit()
