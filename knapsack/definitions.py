import threading
import pygame

pygame.font.init()
FONT = pygame.font.SysFont('monospace', 14)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DELAY = 1 / 10


class Objeto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

        self.mutex = threading.Lock()

    def set_pos(self, pos):
        self.mutex.acquire()

        self.x, self.y = pos

        self.mutex.release()

    def get_pos(self):
        self.mutex.acquire()

        pos = self.x, self.y

        self.mutex.release()

        return pos


class Item(Objeto):
    def __init__(self, valor, peso):
        super(Item, self).__init__(0, 0)

        self.col = 0
        self.linha = 0

        self.valor = valor
        self.peso = peso
        self.dens = valor / peso  # heurística
        self.color = WHITE

        self.text_valor = FONT.render("V:" + str(self.valor), False, BLUE)
        self.text_peso = FONT.render("P:" + str(self.peso), False, BLACK)
        self.text_densidade = FONT.render("D:{:.2f}".format(self.dens), False, RED)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def set_col(self, col):
        self.col = col
        self.set_pos((self.col * (self.width + 5), self.y))

    def set_linha(self, linha):
        self.linha = linha
        self.set_pos((self.x, self.linha * (self.height + 5)))

    def __str__(self):
        return "(P: " + str(self.peso) + ", V: " + str(self.valor) + ", D: " + str(self.dens) + ")"

    def __repr__(self):
        return "(P: " + str(self.peso) + ", V: " + str(self.valor) + ", D: " + str(self.dens) + ")"
