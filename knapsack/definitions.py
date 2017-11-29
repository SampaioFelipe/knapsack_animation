class Item:
    def __init__(self, valor, peso):
        self.valor = valor
        self.peso = peso
        self.dens = valor / peso  # heurística

    def __str__(self):
        return "(P: " + str(self.peso) + ", V: "+ str(self.valor) + ", D: " + str(self.dens) + ")"
    def __repr__(self):
        return "(P: " + str(self.peso) + ", V: "+ str(self.valor) + ", D: " + str(self.dens) + ")"