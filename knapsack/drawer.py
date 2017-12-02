import pygame
import threading

import sys

from knapsack.definitions import *


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
        self.objects_left = None
        self.objects_right = None

        self.FPSCLOCK = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Knapsack Problem')

        self.walle = pygame.image.load("assets/wall-e.png")
        self.logo = pygame.image.load("assets/knapsack-logo.png")

        self.WIN_WIDTH = pygame.display.Info().current_w
        self.WIN_HEIGHT = pygame.display.Info().current_h - 70

        self.walle_pos = (self.WIN_WIDTH // 4 - 75, 10)

        self.DISPLAY = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.greedy_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.dp_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.state = 0

        # Definições dos botões
        BUTTON_FONT = pygame.font.SysFont('monospace', 30)

        # Tela inicial

        text = BUTTON_FONT.render("Começar", True, WHITE)

        self.btn_inicial = Button((self.WIN_WIDTH // 2 - 75, self.WIN_HEIGHT // 2 + 150), (150, 50), text,
                                  BUTTON_FONT.size("Começar"))

        # Tela de Configurações

        # Tela de algoritmos

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

        return True

    def draw_tela_inicial(self):

        self.event_handler(0)

        self.DISPLAY.fill(WHITE)
        center = self.WIN_WIDTH // 2, self.WIN_HEIGHT // 2
        self.DISPLAY.blit(self.logo, (center[0] - 135, center[1] - 150))

        self.btn_inicial.draw(self.DISPLAY)

    def draw_tela_configuracao(self):
        self.event_handler(1)

        self.DISPLAY.fill(WHITE)


    def draw_algoritmos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                            event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mousex, self.mousey = event.pos
                self.mouseClicked = True

        self.DISPLAY.fill((0, 0, 0))

        self.greedy_surface.fill((0, 0, 0))
        self.dp_surface.fill((255, 255, 255))

        self.dp_surface.blit(self.walle, self.walle_pos)
        self.greedy_surface.blit(self.walle, self.walle_pos)

        for obj in self.objects_left:
            self.draw_item_greedy(obj)

        self.DISPLAY.blit(self.greedy_surface, (0, 0))
        self.DISPLAY.blit(self.dp_surface, (self.WIN_WIDTH // 2, 0))

    def draw_item_greedy(self, item):
        pos_x, pos_y = item.get_pos()
        pygame.draw.rect(self.greedy_surface, item.get_current_color(),
                         pygame.Rect(pos_x, pos_y, item.width, item.height))

        self.greedy_surface.blit(item.text_valor, (pos_x, pos_y))
        self.greedy_surface.blit(item.text_peso, (pos_x, pos_y + 15))
        self.greedy_surface.blit(item.text_densidade, (pos_x, pos_y + 30))
