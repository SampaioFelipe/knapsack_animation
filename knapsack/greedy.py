from knapsack.mergesort import mergesort
from knapsack import drawer

def greedy_knapsack(V, C):
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