import pygame

FPSCLOCK = pygame.time.Clock()
DISPLAY = None

class Objeto:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

def init_video_settings():
    global DISPLAY

    pygame.init()
    pygame.display.set_caption('Knapsack Problem')

    WIN_WIDTH = pygame.display.Info().current_w
    WIN_HEIGHT = pygame.display.Info().current_h

    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                        event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            return
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True

def draw():
    pygame.draw.rect(DISPLAY, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
    pygame.display.flip()