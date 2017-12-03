import sys

from knapsack.mergesort import mergesort
from knapsack.definitions import DELAY, RED
import time


def anima_preparacao(V, dimen):
    i = 0
    for item in V:
        item.y = (dimen[1] // 2) + 200
        item.set_col(i)
        i = i + 1


def anima_escolha(item, dimen):
    inc_x = ((dimen[0] // 2) - item.x) // 100
    inc_y = ((dimen[1] // 2) - item.y) // 100

    while item.y > dimen[1] // 2:
        item.x += inc_x
        item.y += inc_y

        time.sleep(DELAY / 50)

    item.x = (dimen[0] // 2) - item.width // 2
    item.y = dimen[1] // 2

    time.sleep(1)


def anima_aceita(item):
    while item.y > 100:
        item.y -= 1
        time.sleep(DELAY / 50)


def anima_recusa(item, pos):
    item.current_color = RED

    inc_x = (pos[0] - item.x) // 100
    inc_y = (pos[1] - item.y) // 100

    while item.y < pos[1]:
        item.x += inc_x
        item.y += inc_y

        time.sleep(DELAY / 50)

    item.x = pos[0]
    item.y = pos[1]

    time.sleep(1)


def greedy_knapsack(itens, capacidade, dimen, args, control):
    anima_preparacao(itens, dimen)

    ordenado = mergesort(itens, control)

    itens = []

    for item in ordenado:

        if control.is_set():
            sys.exit(0)

        pos = item.get_pos()
        anima_escolha(item, dimen)

        if (args['peso_corrente'] + item.peso) <= capacidade:
            anima_aceita(item)
            args['valor_total'] = args['valor_total'] + item.valor
            args['peso_corrente'] = args['peso_corrente'] + item.peso
            itens.append(item)
            if args['peso_corrente'] == capacidade:
                return itens, args['valor_total']
        else:
            anima_recusa(item, pos)

    return itens, args['valor_total']
