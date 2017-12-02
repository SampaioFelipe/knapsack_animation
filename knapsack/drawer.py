import pygame
import threading

import sys

from knapsack.definitions import *


class InputBox:
    def __init__(self, pos, width, label, limit):
        self.pos = pos
        self.dimen = width, 40
        self.label = FONT_INPUT.render(label, True, WHITE)

        self.text = ""

        self.limit = limit

        self.selected = False

    def add_digito(self, letra):
        if self.limit > 0:
            self.text += letra
            self.limit -= 1

    def backspace(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
            self.limit += 1

    def get_value(self):
        if len(self.text) > 0:
            return int(self.text)

        return 0

    def draw(self, surface):
        surface.blit(self.label, (self.pos[0], self.pos[1] - 25))

        text = FONT_INPUT.render(self.text, True, WHITE)

        if self.selected:
            pygame.draw.rect(surface, GREEN, (self.pos + self.dimen), 2)
        else:
            pygame.draw.rect(surface, WHITE, (self.pos + self.dimen), 2)

        surface.blit(text, (self.pos[0] + 10, self.pos[1] + 12))

        return False

    def check_hover(self):
        mouse = pygame.mouse.get_pos()

        if (self.pos[0] < mouse[0] < self.pos[0] + self.dimen[0]) and (
                        self.pos[1] < mouse[1] < self.pos[1] + self.dimen[1]):
            return True

        return False

    def select(self):
        if self.check_hover():
            self.selected = True

        return self.selected

    def deselect(self):
        self.selected = False


class Button:
    def __init__(self, pos, dimen, text, text_size):
        self.pos = pos
        self.dimen = dimen
        self.text = text
        self.text_size = text_size
        self.primary_color = GREEN
        self.secondary_color = (100, 255, 100)

        self.text_pos = (self.pos[0] + (self.dimen[0] - self.text_size[0]) // 2,
                         self.pos[1] + (self.dimen[1] - self.text_size[1]) // 2)

    def set_primary_color(self, color):
        self.primary_color = color

    def set_secondary_color(self, color):
        self.secondary_color = color

    def draw(self, surface):

        if self.check_hover():
            pygame.draw.rect(surface, self.secondary_color, (self.pos + self.dimen))
        else:
            pygame.draw.rect(surface, self.primary_color, (self.pos + self.dimen))

        surface.blit(self.text, self.text_pos)

        return False

    def check_hover(self):
        mouse = pygame.mouse.get_pos()

        if (self.pos[0] < mouse[0] < self.pos[0] + self.dimen[0]) and (
                        self.pos[1] < mouse[1] < self.pos[1] + self.dimen[1]):
            return True

        return False

    def click(self):
        if self.check_hover():
            return True

        return False


class Animation(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.FPSCLOCK = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Knapsack Problem')

        self.logo = pygame.image.load("assets/knapsack-logo.png")

        self.knapsack_grey = pygame.image.load("assets/mochila_cinza.png")
        self.knapsack_greedy = pygame.image.load("assets/mochila_verde.png")
        self.knapsack_dp = pygame.image.load("assets/mochila_vermelha.png")

        self.WIN_WIDTH = pygame.display.Info().current_w
        self.WIN_HEIGHT = pygame.display.Info().current_h - 70

        self.knapsack_pos = (self.WIN_WIDTH // 4 - 75, 20)

        self.DISPLAY = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.greedy_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.dp_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.state = 0

        # Definições dos itens de menu
        BUTTON_FONT = pygame.font.SysFont('monospace', 30)

        # Tela inicial

        text = BUTTON_FONT.render("Começar", True, WHITE)

        self.btn_inicial = Button((self.WIN_WIDTH // 2 - 75, self.WIN_HEIGHT // 2 + 150), (150, 50), text,
                                  BUTTON_FONT.size("Começar"))

        # Tela de Configurações
        self.input_config = {"capacidade": InputBox((15, 50), 150, "CAPACIDADE", 3),
                             "nro_itens": InputBox((15, 150), 150, "QTD ITENS", 3),
                             "peso_min": InputBox((15, 250), 100, "MIN PESO", 3),
                             "peso_max": InputBox((150, 250), 100, "MAX PESO", 3),
                             "valor_min": InputBox((15, 350), 100, "MIN VALOR", 3),
                             "valor_max": InputBox((150, 350), 100, "MAX VALOR", 3)}

        text = BUTTON_FONT.render("INICIAR", True, WHITE)
        self.btn_iniciar_algoritmos = Button((0, self.WIN_HEIGHT - 50), (300, 50), text,
                                             BUTTON_FONT.size("INICIAR"))

        self.input_active = ""

        # Tela de algoritmos
        self.greedy_alg = []
        self.dp_alg = []
        self.current_draw = self.draw_tela_inicial

    def run(self):
        while True:
            try:
                self.current_draw()
                pygame.display.flip()
                self.FPSCLOCK.tick(30)
            except Exception as e:
                print(e)
                return

    def event_handler(self, state):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                            event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:

                if state == 0:
                    if self.btn_inicial.click():
                        self.current_draw = self.draw_tela_configuracao

                elif state == 1:

                    if len(self.input_active) > 0:
                        self.input_config[self.input_active].deselect()
                        self.input_active = ""

                    for (key, obj) in self.input_config.items():
                        if obj.select():
                            self.input_active = key
                            break
                    if self.btn_iniciar_algoritmos.click():
                        self.anima_out_menu()
                        self.current_draw = self.draw_algoritmos

            elif event.type == pygame.KEYDOWN:
                if state == 1:

                    if len(self.input_active) > 0:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_config[self.input_active].backspace()
                        else:
                            try:
                                val = int(pygame.key.name(event.key))
                                self.input_config[self.input_active].add_digito(str(val))
                            except Exception:
                                pass
        return True

    def anima_out_menu(self):
        for i in range(11):
            self.DISPLAY.fill(WHITE)
            pygame.draw.rect(self.DISPLAY, (50, 50, 50), (0, 0, 300 - i * 30, self.WIN_HEIGHT))

            for (_, obj) in self.input_config.items():
                obj.pos = (obj.pos[0] - 30, obj.pos[1])
                obj.draw(self.DISPLAY)

            pygame.time.delay(25)
            pygame.display.flip()

    def anima_in_menu(self):
        for i in range(11):
            self.DISPLAY.fill(WHITE)
            pygame.draw.rect(self.DISPLAY, (50, 50, 50), (0, 0, i * 30, self.WIN_HEIGHT))

            for (_, obj) in self.input_config.items():
                obj.pos = (obj.pos[0] + 30, obj.pos[1])
                obj.draw(self.DISPLAY)

            pygame.time.delay(25)
            pygame.display.flip()

    def draw_tela_inicial(self):

        self.event_handler(0)

        self.DISPLAY.fill(WHITE)
        center = self.WIN_WIDTH // 2, self.WIN_HEIGHT // 2
        self.DISPLAY.blit(self.logo, (center[0] - 135, center[1] - 150))

        self.btn_inicial.draw(self.DISPLAY)

    def draw_tela_configuracao(self):
        self.event_handler(1)

        self.DISPLAY.fill(WHITE)
        pygame.draw.rect(self.DISPLAY, (50, 50, 50), (0, 0, 300, self.WIN_HEIGHT))

        for (_, obj) in self.input_config.items():
            obj.draw(self.DISPLAY)

        self.btn_iniciar_algoritmos.draw(self.DISPLAY)

    def draw_algoritmos(self):
        self.event_handler(2)

        self.DISPLAY.fill(WHITE)

        self.greedy_surface.fill(WHITE)
        self.dp_surface.fill((255, 255, 255))

        # self.dp_surface.blit(self.knapsack_grey, (0, 0, 30, 300), (0, 0, 30, 300))
        self.dp_surface.blit(self.knapsack_grey, self.knapsack_pos)

        self.greedy_surface.blit(self.knapsack_grey, self.knapsack_pos)

        for obj in self.greedy_alg:
            self.draw_item_greedy(obj)

        self.DISPLAY.blit(self.greedy_surface, (0, 0))
        self.DISPLAY.blit(self.dp_surface, (self.WIN_WIDTH // 2, 0))
        pygame.draw.line(self.DISPLAY, BLACK, (self.WIN_WIDTH // 2, 0), (self.WIN_WIDTH // 2, self.WIN_HEIGHT), 5)

    def draw_item_greedy(self, item):
        pos_x, pos_y = item.get_pos()
        pygame.draw.rect(self.greedy_surface, item.get_current_color(),
                         pygame.Rect(pos_x, pos_y, item.width, item.height))

        self.greedy_surface.blit(item.text_valor, (pos_x, pos_y))
        self.greedy_surface.blit(item.text_peso, (pos_x, pos_y + 15))
        self.greedy_surface.blit(item.text_densidade, (pos_x, pos_y + 30))
