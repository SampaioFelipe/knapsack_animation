import time
from knapsack.definitions import *

def anima_escolhe(item, col):
    item.set_col(col)
    item.inc_linha()

    item.restore_color()

    time.sleep(DELAY)


def anima_retorna(itens):
    for item in itens:
        item.dec_linha()

    time.sleep(DELAY)


def anima_comparacao(item1, item2):
    item1.set_current_color(GREEN)
    item2.set_current_color(GREEN)

    time.sleep(DELAY)


def mergesort(itens):
    tamanho = len(itens)

    if tamanho < 2:
        return itens

    else:

        parcial_left = mergesort(itens[:tamanho // 2])
        parcial_right = mergesort(itens[tamanho // 2:])

        resultado = []

        cur_col = parcial_left[0].get_col()

        while (len(parcial_left) > 0) and (len(parcial_right) > 0):

            anima_comparacao(parcial_left[0], parcial_right[0])

            if parcial_left[0].dens > parcial_right[0].dens:
                anima_escolhe(parcial_left[0], cur_col)
                resultado.append(parcial_left.pop(0))
            else:
                anima_escolhe(parcial_right[0], cur_col)
                resultado.append(parcial_right.pop(0))

            cur_col = cur_col + 1

        if len(parcial_left) > 0:
            restante = parcial_left
        else:
            restante = parcial_right

        resultado += restante

        for item in restante:
            anima_comparacao(item, item)
            anima_escolhe(item, cur_col)
            cur_col += 1

        anima_retorna(resultado)

        return resultado
