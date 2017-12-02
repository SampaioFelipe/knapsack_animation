import time
from knapsack.definitions import *


# def anima_troca(item1, item2):
#     item1.inc_linha()
#     item2.inc_linha()
#
#     p1 = item1.get_pos()
#     p2 = item2.get_pos()
#
#     i = 0
#     j = 0
#
#     while item1.get_pos()[0] != p2[0]:
#         item1.set_pos((p1[0] + i, p1[1]))
#         item2.set_pos((p2[0] - j, p2[1]))
#
#         i = i + 1
#         j = j + 1
#
#         time.sleep(DELAY / 100)
#
#     item1.dec_linha()
#     item2.dec_linha()


def anima_escolhe(item, col, color):
    item.set_col(col)
    item.inc_linha()

    item.set_final_color(color)
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
        for item in itens[:tamanho // 2]:
            r, g, b = item.get_final_color()
            item.set_final_color((r - 10, g - 10, b))
            item.restore_color()

        for item in itens[tamanho // 2:]:
            r, g, b = item.get_final_color()
            item.set_final_color((r, g - 10, b - 10))
            item.restore_color()

        parcial_left = mergesort(itens[:tamanho // 2])
        parcial_right = mergesort(itens[tamanho // 2:])

        resultado = []

        cur_col = parcial_left[0].get_col()
        final_color = parcial_left[0].get_final_color()

        while (len(parcial_left) > 0) and (len(parcial_right) > 0):

            anima_comparacao(parcial_left[0], parcial_right[0])

            if parcial_left[0].dens > parcial_right[0].dens:
                anima_escolhe(parcial_left[0], cur_col, final_color)
                resultado.append(parcial_left.pop(0))
            else:
                anima_escolhe(parcial_right[0], cur_col, final_color)
                resultado.append(parcial_right.pop(0))

            cur_col = cur_col + 1

        if len(parcial_left) > 0:
            restante = parcial_left
        else:
            restante = parcial_right

        resultado += restante

        for item in restante:
            anima_comparacao(item, item)
            anima_escolhe(item, cur_col, final_color)
            cur_col += 1

        anima_retorna(resultado)

        for item in itens[:tamanho // 2]:
            r, g, b = item.get_final_color()
            item.set_final_color((r + 10, g + 10, b))

        for item in itens[tamanho // 2:]:
            r, g, b = item.get_final_color()
            item.set_final_color((r, g + 10, b + 10))

        return resultado
