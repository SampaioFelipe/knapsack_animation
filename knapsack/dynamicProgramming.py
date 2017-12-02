

def dynamicProgramming_knapsack(Itens, C):
    K = [[0 for x in range(C+1)] for x in range(len(Itens)+1)]

    for i in range(len(Itens)+1):
        for p in range(C+1):
            if i == 0 or p == 0:
                K[i][p] = 0
            elif Itens[i-1].peso <= p:
                K[i][p] = max(Itens[i-1].valor + K[i-1][p-Itens[i-1].peso], K[i-1][p])
            else:
                K[i][p] = K[i - 1][p]

    return K[len(Itens)][C]
