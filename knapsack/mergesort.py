from knapsack import drawer

def mergesort(V):

    drawer.pygame.draw.rect(drawer.DISPLAY, (0, 0, 255), drawer.pygame.Rect(70, 70, 60, 60))

    tamanho = len(V)

    if tamanho < 3:
        if tamanho == 1:
            return V

        else:
            if V[0].dens < V[1].dens:
                aux = V[0]
                V[0] = V[1]
                V[1] = aux

            return V
    else:
        parcial_left = mergesort(V[:tamanho // 2])
        parcial_right = mergesort(V[tamanho // 2:])

        resultado = []
        while (len(parcial_left) > 0) and (len(parcial_right) > 0):
            if (parcial_left[0].dens > parcial_right[0].dens):
                resultado.append(parcial_left.pop(0))
            else:
                resultado.append(parcial_right.pop(0))

        resultado += parcial_left + parcial_right

        return resultado
