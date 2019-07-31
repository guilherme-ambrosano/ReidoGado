import pygame
import random


class Piquete():
    def __init__(self, env, num):
        self.env = env
        self.preco_irrig = self.env.preco_irrig
        self.num = num
        self.irrig_instalada = False
        self.irrigado = False
        self.bois = 0
        self.p_x = 0
        self.p_y = 0
        self.p_hei = 0
        self.p_wid = 0
        self.forragem = 1000
        self.grama = 3
        self.sprite_x = None
        self.sprite_y = None
        self.unidades_sprite_x = None
        self.unidades_sprite_y = None
        self.especie = random.randint(1, 4)

    def resetar_preco_irrig(self):
        self.preco_irrig = self.env.preco_irrig

    def descontar_irrig(self):
        custo = 0
        if self.irrigado:
            if not self.irrig_instalada:
                custo += self.env.preco_instal_irrig
                self.irrig_instalada = True
            custo += self.preco_irrig
            self.preco_irrig = 0 # p não cobrar mais de 1 vez
        return custo

    def set_irrig(self):
        self.irrigado = not self.irrigado

    def adicionar_bois(self):
        if self.env.bois > 0:
            self.bois += 1
            self.env.remover_bois()

    def remover_bois(self):
        if self.bois > 0:
            self.bois -= 1
            self.env.adicionar_bois()

    def atualizar_coord(self):

        croq = self.env.get_croqui()
        self.p_wid = 650/croq[0] - 5
        self.p_hei = 350/croq[1] - 5


        unidades_x = self.num%croq[0]
        unidades_y = self.num//croq[0]

        self.p_x = 75 + unidades_x*650/croq[0]
        self.p_y = 75 + unidades_y*350/croq[1]

        if self.unidades_sprite_x is None and\
                self.unidades_sprite_y is None and\
                self.sprite_x is None and self.sprite_y is None:
            self.unidades_sprite_x = random.randint(0,
                                       self.env.piquetes-1)%croq[0]
            self.unidades_sprite_y = random.randint(0,
                                      self.env.piquetes-1)//croq[0]

            self.sprite_x = max(0, self.unidades_sprite_x*650/
                                                      croq[0] - 75)

            self.sprite_y = max(0, self.unidades_sprite_y*350/
                                                      croq[1] - 75)


    def simular_clima(self, taxa):
        self.env.calculo_diario(taxa)
        # self.env.simular_temperatura()
        # self.env.simular_chuva()

    def cresc_grama_1(self, irrigacao, taxa):
        self.simular_clima(taxa)
        # print(self.env.temperatura)
        # print(self.env.chuva)

        #TODO trocar isso por um balanço hidrico sério
        if self.env.chuva[-1]/taxa > 100:
            irrigacao = 1.5
        self.forragem += 0.5*irrigacao*taxa
        self.forragem -= 0.25*self.bois*taxa
        self.forragem = max(0, self.forragem)

    def atualizar_grama(self):
        # PROVAVELMENTE VAI TER QUE MODIFICAR
        # TODO modificar
        if self.env.fast_forward:
            taxa = 15
        else:
            taxa = 1

        if self.irrigado:
            irrigacao = 1.5
        else:
            irrigacao = 1

        if self.especie == 1:
            self.cresc_grama_1(irrigacao, taxa)
        elif self.especie == 2:
            self.cresc_grama_1(irrigacao, taxa)
        elif self.especie == 3:
            self.cresc_grama_1(irrigacao, taxa)
        elif self.especie == 4:
            self.cresc_grama_1(irrigacao, taxa)

        if self.forragem >= 1000:
            self.grama = 3
        elif self.forragem >= 750 and self.forragem < 1000:
            self.grama = 2
        elif self.forragem >= 500 and self.forragem < 1000:
            self.grama = 1
        elif self.forragem < 500:
            self.grama = 0

    def draw(self, win):
        sem_grama = pygame.image.load("../Sprites/Ambiente/"
                                      "Grama/sem_grama.png")
        grama_baixa = pygame.image.load("../Sprites/Ambiente/"
                                        "Grama/grama_baixa.png")
        grama_media = pygame.image.load("../Sprites/Ambiente/"
                                        "Grama/grama_media.png")
        grama_alta = pygame.image.load("../Sprites/Ambiente/"
                                       "Grama/grama_alta.png")

        self.atualizar_coord()
        cropped = pygame.Surface((self.p_wid, self.p_hei))

        if self.grama == 0:
            cropped.blit(sem_grama, (0, 0),
                         (self.sprite_x, self.sprite_y,
                             self.p_wid, self.p_hei))
            win.blit(cropped, (self.p_x, self.p_y))

        elif self.grama == 1:
            cropped.blit(grama_baixa, (0, 0),
                         (self.sprite_x, self.sprite_y,
                             self.p_wid, self.p_hei))
            win.blit(cropped, (self.p_x, self.p_y))

        elif self.grama == 2:
            cropped.blit(grama_media, (0, 0),
                         (self.sprite_x, self.sprite_y,
                             self.p_wid, self.p_hei))
            win.blit(cropped, (self.p_x, self.p_y))

        elif self.grama == 3:
            cropped.blit(grama_alta, (0, 0),
                         (self.sprite_x, self.sprite_y,
                             self.p_wid, self.p_hei))
            win.blit(cropped, (self.p_x, self.p_y))

    def is_over(self, pos):
        # mouse sobre o piquete
        if pos[0] > self.p_x and pos[0] < self.p_x + self.p_wid:
            if pos[1] > self.p_y and\
                    pos[1] < self.p_y + self.p_hei:
                return True
        return False
