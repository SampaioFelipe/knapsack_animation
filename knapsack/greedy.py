from knapsack.mergesort import mergesort
from knapsack.definitions import DELAY
import time


def anima_preparacao(V):
    i = 0
    for item in V:
        item.set_linha(2)
        i = i + 1

        time.sleep(DELAY)


def greedy_knapsack(V, C):
    anima_preparacao(V)

    ordenado = mergesort(V)

    peso_total = ordenado[0].peso
    valor_total = ordenado[0].valor

    itens = [ordenado[0]]

    for item in ordenado[1:]:
        if (peso_total + item.peso) <= C:
            valor_total = valor_total + item.valor
            peso_total = peso_total + item.peso
            itens.append(item)

            if peso_total == C:
                return itens, valor_total

    return itens, valor_total
