import pygame
import threading
from knapsack.definitions import *


class Animation(threading.Thread):
    def __init__(self, objs_left, objs_right):
        threading.Thread.__init__(self)
        self.objects_left = objs_left
        self.objects_right = objs_right

        self.FPSCLOCK = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Knapsack Problem')

        self.walle = pygame.image.load("/home/felipe/PycharmProjects/projeto_paa/assets/wall-e.png")

        self.WIN_WIDTH = pygame.display.Info().current_w
        self.WIN_HEIGHT = pygame.display.Info().current_h - 75

        self.walle_pos = (self.WIN_WIDTH//4 - 75, 10)

        self.DISPLAY = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.greedy_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.dp_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

    def run(self):
        while self.event_handler():
            try:

                self.draw()
                self.FPSCLOCK.tick(30)
            except Exception as e:
                print(e)
                return

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                            event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        return True

    def draw(self):
        self.DISPLAY.fill((0, 0, 0))

        self.greedy_surface.fill((0, 0, 0))
        self.dp_surface.fill((255, 255, 255))

        self.dp_surface.blit(self.walle, self.walle_pos)
        self.greedy_surface.blit(self.walle, self.walle_pos)

        for obj in self.objects_left:
            self.draw_item_greedy(obj)

        self.DISPLAY.blit(self.greedy_surface, (0, 0))
        self.DISPLAY.blit(self.dp_surface, (self.WIN_WIDTH // 2, 0))

        pygame.display.flip()

    def draw_item_greedy(self, item):
        pos_x, pos_y = item.get_pos()
        pygame.draw.rect(self.greedy_surface, item.get_color(), pygame.Rect(pos_x, pos_y, item.width, item.height))

        self.greedy_surface.blit(item.text_valor, (pos_x, pos_y))
        self.greedy_surface.blit(item.text_peso, (pos_x, pos_y + 15))
        self.greedy_surface.blit(item.text_densidade, (pos_x, pos_y + 30))



