from knapsack.mergesort import mergesort
from knapsack.definitions import DELAY
import time


def anima_preparacao(V, initial_line):
    i = 0
    for item in V:
        item.set_linha(initial_line)
        i = i + 1

        time.sleep(DELAY)

# def anima_escolha(item):
#
#


def greedy_knapsack(itens, capacidade):
    anima_preparacao(itens, 6)

    ordenado = mergesort(itens)

    peso_total = ordenado[0].peso
    valor_total = ordenado[0].valor

    itens = [ordenado[0]]

    for item in ordenado[1:]:
        if (peso_total + item.peso) <= capacidade:
            valor_total = valor_total + item.valor
            peso_total = peso_total + item.peso
            itens.append(item)

            if peso_total == capacidade:
                return itens, valor_total

    return itens, valor_total
