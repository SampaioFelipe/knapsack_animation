import time
from knapsack.definitions import *


def anima_troca(item1, item2):
    item1.set_linha(item1.linha + 1)
    item2.set_linha(item2.linha + 1)

    p1 = item1.get_pos()
    p2 = item2.get_pos()

    i = 0
    j = 0

    while item1.get_pos()[0] != p2[0]:
        item1.set_pos((p1[0] + i, p1[1]))
        item2.set_pos((p2[0] - j, p2[1]))

        i = i + 1
        j = j + 1

        time.sleep(DELAY/20)

    item1.set_linha(item1.linha - 1)
    item2.set_linha(item2.linha - 1)


def anima_comparacao(item1, item2):
    item1.set_linha(4)
    item2.set_linha(4)

    item1.set_color(GREEN)
    item2.set_color(GREEN)

    time.sleep(1)

    item1.set_color(WHITE)
    item2.set_color(WHITE)


def mergesort(V):
    tamanho = len(V)

    if tamanho < 2:

        V[0].set_linha(3)
        time.sleep(1)

        return V

    else:
        parcial_left = mergesort(V[:tamanho // 2])
        parcial_right = mergesort(V[tamanho // 2:])

        resultado = []

        while (len(parcial_left) > 0) and (len(parcial_right) > 0):

            anima_comparacao(parcial_left[0], parcial_right[0])

            if parcial_left[0].dens > parcial_right[0].dens:
                resultado.append(parcial_left.pop(0))
            else:
                anima_troca(parcial_left[0], parcial_right[0])
                resultado.append(parcial_right.pop(0))


        resultado += parcial_left + parcial_right
        print(resultado)
    return resultado
