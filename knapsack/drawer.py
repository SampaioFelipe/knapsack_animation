import sys

from knapsack.definitions import *
from random import randrange

from knapsack.greedy import greedy_knapsack
from knapsack.dynamicProgramming import dynamicProgramming_knapsack


class InputBox:
    def __init__(self, pos, width, label, limit, valor_limite = None):
        self.pos = pos
        self.dimen = width, 40
        self.label = FONT_INPUT.render(label, True, WHITE)

        self.text = ""

        self.valid = True

        self.limit = limit

        self.valor_limite = valor_limite

        self.selected = False

    def set_valid(self):
        self.valid = True

    def set_invalid(self):
        self.valid = False

    def is_valid(self):
        return self.valid

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
            if self.valid:
                pygame.draw.rect(surface, WHITE, (self.pos + self.dimen), 2)
            else:
                pygame.draw.rect(surface, RED, (self.pos + self.dimen), 2)

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

        if self.valor_limite is not None:
            if self.get_value() > self.valor_limite:
                self.set_invalid()
            else:
                self.set_valid()
        else:
            self.set_valid()


class Button:
    def __init__(self, pos, dimen, text, text_size):
        self.pos = pos
        self.dimen = dimen
        self.text = text
        self.text_size = text_size
        self.primary_color = GREEN
        self.secondary_color = (38, 127, 39)

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

        self.maior = 0
        self.peso_dp = 0

        pygame.init()
        pygame.display.set_caption('Knapsack Problem')

        self.logo = pygame.image.load("assets/knapsack-logo.png")

        self.knapsack_grey = pygame.image.load("assets/mochila_cinza.png")

        # Greedy
        self.knapsack_greedy = pygame.image.load("assets/mochila_verde.png")
        self.greedy_capacidade = 0
        self.greedy_args = None

        self.knapsack_dp = pygame.image.load("assets/mochila_vermelha.png")

        self.WIN_WIDTH = pygame.display.Info().current_w
        self.WIN_HEIGHT = pygame.display.Info().current_h - 70

        self.knapsack_pos = (self.WIN_WIDTH // 4 - 75, 20)

        self.DISPLAY = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.greedy_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.dp_surface = pygame.Surface((self.WIN_WIDTH // 2, self.WIN_HEIGHT))

        self.state = 0

        # Definições dos itens de menu

        # Tela inicial

        text = BUTTON_FONT.render("COMEÇAR", True, WHITE)

        self.btn_inicial = Button((self.WIN_WIDTH // 2 - 75, self.WIN_HEIGHT // 2 + 150), (150, 50), text,
                                  BUTTON_FONT.size("COMEÇAR"))

        # Tela de Configurações
        self.input_config = {"capacidade": InputBox((10, 50), 150, "CAPACIDADE", 2, 40),
                             "qtd_itens": InputBox((10, 150), 150, "QTD ITENS", 2, 30),
                             "peso_min": InputBox((10, 250), 100, "MIN PESO", 3),
                             "peso_max": InputBox((135, 250), 100, "MAX PESO", 3),
                             "valor_min": InputBox((10, 350), 100, "MIN VALOR", 3),
                             "valor_max": InputBox((135, 350), 100, "MAX VALOR", 3)}

        text = BUTTON_FONT.render("GERAR", True, WHITE)
        self.btn_gerar_itens = Button((0, self.WIN_HEIGHT - 100), (250, 50), text,
                                      BUTTON_FONT.size("GERAR"))
        self.btn_gerar_itens.set_primary_color((0, 175, 204))
        self.btn_gerar_itens.set_secondary_color((0, 109, 127))

        text = BUTTON_FONT.render("INICIAR", True, WHITE)
        self.btn_iniciar_algoritmos = Button((0, self.WIN_HEIGHT - 50), (250, 50), text,
                                             BUTTON_FONT.size("INICIAR"))

        text = BUTTON_FONT.render("VOLTAR", True, WHITE)
        self.btn_voltar = Button((self.WIN_WIDTH // 2 - 60, self.WIN_HEIGHT - 70), (120, 50), text,
                                 BUTTON_FONT.size("VOLTAR"))
        self.btn_voltar.set_primary_color(RED)
        self.btn_voltar.set_secondary_color((200, 50, 50))

        self.input_active = ""

        # Tela de algoritmos
        self.greedy_alg = []
        self.greedy_thread = None
        self.greedy_thread_event = None

        self.dp_alg = []
        self.dp_k = []
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

    def gera_itens(self):
        self.greedy_alg = []
        self.dp_alg = []
        self.dp_k = []

        self.greedy_args = {'valor_total': 0, 'peso_corrente': 0}

        self.greedy_capacidade = self.input_config["capacidade"].get_value()

        qtd = self.input_config["qtd_itens"].get_value()
        peso_min = self.input_config["peso_min"].get_value()
        peso_max = self.input_config["peso_max"].get_value()
        valor_min = self.input_config["valor_min"].get_value()
        valor_max = self.input_config["valor_max"].get_value()

        for i in range(qtd):
            valor = randrange(valor_min, valor_max)
            peso = randrange(peso_min, peso_max)
            color = (randrange(70, 220), randrange(70, 220), randrange(70, 220))

            item_greedy = Item(valor, peso)
            item_dp = Item(valor, peso)

            item_greedy.set_final_color(color)
            item_greedy.restore_color()

            item_dp.set_final_color(color)
            item_dp.restore_color()

            self.greedy_alg.append(item_greedy)
            self.dp_alg.append(item_dp)

        pos_x = 260
        linha = 0

        for item in self.greedy_alg:

            if pos_x >= self.WIN_WIDTH - item.width:
                pos_x = 260
                linha += 1
            item.set_pos((pos_x, 0))
            item.set_linha(linha)
            item.y += 5
            pos_x += item.width + 5

        self.dp_k = [[0 for x in range(self.input_config["capacidade"].get_value() + 1)] for x in
                     range(len(self.dp_alg) + 1)]

    def valida_inputs(self):
        if self.input_config["capacidade"].is_valid() and self.input_config["capacidade"].get_value() > 0:
            if self.input_config["qtd_itens"].is_valid() and self.input_config["qtd_itens"].get_value() > 0:
                if self.input_config["peso_min"].get_value() < self.input_config["peso_max"].get_value():
                    if self.input_config["valor_min"].get_value() < self.input_config["valor_max"].get_value():
                        return True
                    else:
                        self.input_config["valor_min"].set_invalid()
                        self.input_config["valor_max"].set_invalid()
                else:
                    self.input_config["peso_min"].set_invalid()
                    self.input_config["peso_max"].set_invalid()
            else:
                self.input_config["qtd_itens"].set_invalid()
        else:
            self.input_config["capacidade"].set_invalid()

        return False

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
                        if len(self.greedy_alg) > 0:

                            self.anima_out_menu()

                            if len(self.greedy_alg) > 12:
                                tam_cons = (self.WIN_WIDTH // 2) // len(self.greedy_alg)

                                for item in self.greedy_alg:
                                    item.set_size(tam_cons)

                            self.greedy_thread_event = threading.Event()

                            self.greedy_thread = threading.Thread(target=greedy_knapsack,
                                                                  kwargs={'itens': self.greedy_alg,
                                                                          'capacidade': self.greedy_capacidade,
                                                                          'dimen': (
                                                                              self.WIN_WIDTH // 2, self.WIN_HEIGHT),
                                                                          'args': self.greedy_args,
                                                                          'control': self.greedy_thread_event})

                            dp = threading.Thread(target=dynamicProgramming_knapsack,
                                                  kwargs={'Itens': self.dp_alg,
                                                          'K': self.dp_k,
                                                          'C': self.input_config["capacidade"].get_value()})
                            dp.start()

                            self.greedy_thread.start()

                            self.current_draw = self.draw_algoritmos

                    if self.btn_gerar_itens.click():
                        if self.valida_inputs():
                            self.gera_itens()

                elif state == 2:
                    if self.btn_voltar.click():
                        self.greedy_thread_event.set()
                        self.greedy_alg = []

                        self.dp_alg = []
                        self.dp_k = []
                        self.maior = 0
                        self.peso_dp = 0

                        self.anima_in_menu()

                        self.current_draw = self.draw_tela_configuracao

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
            pygame.draw.rect(self.DISPLAY, (50, 50, 50), (0, 0, 250 - i * 25, self.WIN_HEIGHT))

            for (_, obj) in self.input_config.items():
                obj.pos = (obj.pos[0] - 25, obj.pos[1])
                obj.draw(self.DISPLAY)

            pygame.time.delay(25)
            pygame.display.flip()

    def anima_in_menu(self):
        for i in range(11):
            self.DISPLAY.fill(WHITE)
            pygame.draw.rect(self.DISPLAY, (50, 50, 50), (0, 0, i * 25, self.WIN_HEIGHT))

            for (_, obj) in self.input_config.items():
                obj.pos = (obj.pos[0] + 25, obj.pos[1])
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
        pygame.draw.rect(self.DISPLAY, (50, 50, 50), (0, 0, 250, self.WIN_HEIGHT))

        for (_, obj) in self.input_config.items():
            obj.draw(self.DISPLAY)

        for item in self.greedy_alg:
            self.draw_item(item, self.DISPLAY)

        self.btn_iniciar_algoritmos.draw(self.DISPLAY)
        self.btn_gerar_itens.draw(self.DISPLAY)

    def draw_algoritmos(self):

        self.event_handler(2)

        self.DISPLAY.fill(WHITE)
        # Greedy
        self.greedy_surface.fill(WHITE)

        for obj in self.greedy_alg:
            self.draw_item(obj, self.greedy_surface)

        self.greedy_surface.blit(self.knapsack_greedy, self.knapsack_pos)

        pos = (self.greedy_args['peso_corrente'] * 165) // self.greedy_capacidade
        self.greedy_surface.blit(self.knapsack_grey, (self.knapsack_pos[0], self.knapsack_pos[1] - pos, 150, 10),
                                 (0, -pos, 150, 165))

        greedy_text_valor = BUTTON_FONT.render("$" + str(self.greedy_args['valor_total']).zfill(2), True, GREEN)

        self.greedy_surface.blit(greedy_text_valor, (self.knapsack_pos[0] + 40, self.knapsack_pos[1] + 200))

        greedy_text_capacidade = BUTTON_FONT.render(
            str(self.greedy_args['peso_corrente']).zfill(2) + "/" + str(self.greedy_capacidade).zfill(2), True, GREEN)

        self.greedy_surface.blit(greedy_text_capacidade, (self.knapsack_pos[0] + 240, self.knapsack_pos[1] + 60))

        self.DISPLAY.blit(self.greedy_surface, (0, 0))

        # Fim greedy

        # DP
        self.dp_surface.fill(WHITE)

        self.dp_surface.blit(self.knapsack_dp, self.knapsack_pos)

        pos = (self.peso_dp * 165) // self.input_config["capacidade"].get_value()
        self.dp_surface.blit(self.knapsack_grey, (self.knapsack_pos[0], self.knapsack_pos[1] - pos, 150, 10),
                             (0, -pos, 150, 165))

        dp_text_valor = BUTTON_FONT.render("$" + str(self.maior).zfill(2), True, GREEN)

        self.dp_surface.blit(dp_text_valor, (self.knapsack_pos[0] + 40, self.knapsack_pos[1] + 200))

        dp_text_capacidade = BUTTON_FONT.render(str(self.peso_dp).zfill(2) + "/" + str(self.greedy_capacidade).zfill(2),
                                                True, GREEN)
        self.dp_surface.blit(dp_text_capacidade, (self.knapsack_pos[0] + 240, self.knapsack_pos[1] + 60))

        if len(self.dp_alg) > 0:
            self.draw_dp(self.dp_alg, self.dp_k)

        self.DISPLAY.blit(self.dp_surface, (self.WIN_WIDTH // 2, 0))
        # Fim dp

        pygame.draw.line(self.DISPLAY, BLACK, (self.WIN_WIDTH // 2, 0), (self.WIN_WIDTH // 2, self.WIN_HEIGHT), 5)
        self.btn_voltar.draw(self.DISPLAY)

    def draw_item(self, item, surface):
        pos_x, pos_y = item.get_pos()
        pygame.draw.rect(surface, item.get_current_color(),
                         pygame.Rect(pos_x, pos_y, item.width, item.height))

        if item.show_text is True:
            surface.blit(item.text_valor, (pos_x, pos_y))
            surface.blit(item.text_peso, (pos_x, pos_y + 15))
            surface.blit(item.text_densidade, (pos_x, pos_y + 30))

    def draw_dp(self, itens, K):
        tamanho_quadrado = 50

        posicao = 15

        if (len(K[0]) > 10):
            tamanho_quadrado = self.dp_surface.get_width() // (len(K[0]) + 4)
            posicao = 0
        if (len(itens) > 8):
            tamanho_quadrado = self.dp_surface.get_height() // (len(itens) + 20)
            posicao = 0

        pos_x = self.dp_surface.get_height() // 2 - tamanho_quadrado * (len(K[0]) + 2) // 2
        pos_y = self.dp_surface.get_width() // 2 - 90

        for i in range(0, len(K[0])):
            pygame.draw.rect(self.dp_surface, BLACK,
                             pygame.Rect(pos_x + i * (tamanho_quadrado + tamanho_quadrado // 10), pos_y,
                                         tamanho_quadrado, tamanho_quadrado))
            if (i != 0):
                texto = FONT.render(str(i), False, WHITE)
                self.dp_surface.blit(texto, (
                    pos_x + posicao + i * (tamanho_quadrado + (tamanho_quadrado // 10)), pos_y + posicao))

        pos_y = pos_y + 5
        y = 1
        for i in itens:
            i.height = tamanho_quadrado
            i.width = tamanho_quadrado
            if (tamanho_quadrado < 50):
                i.show_text = False
            i.set_pos((pos_x, pos_y + y * (tamanho_quadrado + (tamanho_quadrado // 10))))
            self.draw_item(i, self.dp_surface)
            y = y + 1

        for i in range(1, len(K)):
            for j in range(1, len(K[i])):
                if (K[i][j] > self.maior):
                    self.peso_dp = j
                if (K[i][j] >= self.maior):
                    self.maior = K[i][j]
                    pygame.draw.rect(self.dp_surface, RED,
                                     pygame.Rect(pos_x + j * (tamanho_quadrado + tamanho_quadrado // 10),
                                                 pos_y + i * (tamanho_quadrado + tamanho_quadrado // 10),
                                                 tamanho_quadrado, tamanho_quadrado))

                    if (j <= self.peso_dp):
                        pygame.draw.rect(self.dp_surface, GREEN,
                                         pygame.Rect(pos_x + j * (tamanho_quadrado + tamanho_quadrado // 10),
                                                     pos_y + i * (tamanho_quadrado + tamanho_quadrado // 10),
                                                     tamanho_quadrado, tamanho_quadrado))
                        self.peso_dp = j
                else:
                    pygame.draw.rect(self.dp_surface, BLUE,
                                     pygame.Rect(pos_x + j * (tamanho_quadrado + tamanho_quadrado // 10),
                                                 pos_y + i * (tamanho_quadrado + tamanho_quadrado // 10),
                                                 tamanho_quadrado, tamanho_quadrado))
                texto = FONT.render(str(K[i][j]), False, WHITE)
                self.dp_surface.blit(texto, (pos_x + posicao + j * (tamanho_quadrado + (tamanho_quadrado // 10)),
                                             pos_y + posicao + i * (tamanho_quadrado + (tamanho_quadrado // 10))))
