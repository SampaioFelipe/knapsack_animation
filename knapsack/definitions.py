import threading
import pygame

pygame.font.init()

FONT = pygame.font.SysFont('monospace', 14)

FONT_INPUT = pygame.font.SysFont('monospace', 20)

BUTTON_FONT = pygame.font.SysFont('monospace', 30)

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

        self.fator_linha = self.height + 5
        self.fator_col = self.width + 5

        self.valor = valor
        self.peso = peso
        self.dens = valor / peso
        self.final_color = (50, 50, 50)
        self.current_color = (50, 50, 50)

        self.text_valor = FONT.render("V:" + str(self.valor), True, BLACK)
        self.text_peso = FONT.render("P:" + str(self.peso), True, BLACK)
        self.text_densidade = FONT.render("D:{:.1f}".format(self.dens), True, BLACK)

        self.show_text = True

    def get_current_color(self):

        return self.current_color

    def set_current_color(self, color):
        self.current_color = color

    def get_final_color(self):
        return self.final_color

    def set_final_color(self, color):
        self.final_color = color

    def restore_color(self):
        self.current_color = self.final_color

    def set_col(self, col):
        self.set_pos((col * self.fator_col, self.y))

    def get_col(self):
        return self.x // self.fator_col

    def set_linha(self, linha):
        self.set_pos((self.x, linha * self.fator_linha))

    def inc_linha(self):
        self.set_pos((self.x, self.y + self.fator_linha))

    def dec_linha(self):
        self.set_pos((self.x, self.y - self.fator_linha))

    def inc_col(self):
        self.set_pos((self.x + self.fator_col, self.y))

    def dec_col(self):
        self.set_pos((self.x - self.fator_col, self.y))

    def set_size(self, size):
        print("setting")
        print(size)
        if size < 50:
            self.show_text = False
        else:
            self.show_text = True

        self.width = size - 5
        self.height = size - 5

        self.fator_linha = self.height + 5
        self.fator_col = self.width + 5

    def __str__(self):
        return "(P: " + str(self.peso) + ", V: " + str(self.valor) + ", D: " + str(self.dens) + ")"

    def __repr__(self):
        return "(P: " + str(self.peso) + ", V: " + str(self.valor) + ", D: " + str(self.dens) + ")"
