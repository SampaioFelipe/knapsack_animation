from knapsack.mergesort import mergesort
from knapsack.definitions import DELAY
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

        time.sleep(DELAY/50)

    item.x = dimen[0] // 2
    item.y = dimen[1] // 2

    time.sleep(1)

def anima_aceita(item):
    while item.y < 100 // 2:
        item.y -= 1

        time.sleep(DELAY/50)


def greedy_knapsack(itens, capacidade, dimen):
    anima_preparacao(itens, dimen)

    ordenado = mergesort(itens)

    peso_total = ordenado[0].peso
    valor_total = ordenado[0].valor

    itens = [ordenado[0]]

    for item in ordenado[1:]:
        anima_escolha(item, dimen)
        ordenado.pop(0)
        if (peso_total + item.peso) <= capacidade:
            anima_aceita(item)
            valor_total = valor_total + item.valor
            peso_total = peso_total + item.peso
            itens.append(item)
            if peso_total == capacidade:
                return itens, valor_total
        # else:


    return itens, valor_total
