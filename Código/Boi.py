import pygame
import random


class Boi():
    def __init__(self, piquete):
        self.piq = piquete
        self.x = self.piq.p_x + 0.5*self.piq.p_wid
        self.y = self.piq.p_y + 0.5*self.piq.p_hei
        self.x_antigo = None
        self.y_antigo = None
        self.wid_antigo = None
        self.hei_antigo = None
        self.peso = 40
        self.idade = 0

    def atualizar_idade(self):
        # Idade dos bois
        # N to usando pra nada, mas pode ser util
        if self.piq.env.fast_forward:
            taxa = 15
        else:
            taxa = 1
        self.idade += taxa

    def atualizar_peso(self):
        # PROVAVELMENTE VAI PRECISAR MODIFICAR
        if self.piq.env.fast_forward:
            taxa = 15
        else:
            taxa = 1

        if self.piq.grama == 0:
            self.peso = max(0, self.peso - 5*taxa)
        elif self.piq.grama == 1:
            self.peso = min(100, self.peso + 0)
        elif self.piq.grama == 2:
            self.peso = min(100, self.peso + 5*taxa)
        elif self.piq.grama == 3:
            self.peso = min(100, self.peso + 10*taxa)

    def get_antigos(self):
        # Pegando as coordenadas antigas do piquete pra se
        # comprar um piquete novo com os bois dentro do antigo
        self.x_antigo = self.piq.p_x
        self.y_antigo = self.piq.p_y
        self.wid_antigo = self.piq.p_wid
        self.hei_antigo = self.piq.p_hei

    def reset(self):
        # Ajustar coordenada do boi no croqui novo
        # se comprar um piquete novo com os bois dentro
        self.piq.atualizar_coord()

        self.x = self.piq.p_x + (self.x - self.x_antigo)*\
                self.piq.p_wid/self.wid_antigo

        self.y = self.piq.p_y + (self.y - self.y_antigo)*\
                self.piq.p_hei/self.hei_antigo

    def update(self):
        # Movimento dos bois
        if self.piq.env.fast_forward:
            taxa = 15
        else:
            taxa = 1
        self.x += random.choice([-1, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, +1])*taxa

        self.y += random.choice([-1, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, +1])*taxa

        if self.x > (self.piq.p_x+self.piq.p_wid - 15):
            self.x -= 2*taxa
            self.y += random.choice([-1, +1])*taxa
        elif self.x < (self.piq.p_x + 15):
            self.x += 2*taxa
            self.y += random.choice([-1, +1])*taxa

        if self.y > (self.piq.p_y+self.piq.p_hei - 15):
            self.y -= 2*taxa
            self.x += random.choice([-1, +1])*taxa
        elif self.y < (self.piq.p_y + 15):
            self.y += 2*taxa
            self.x += random.choice([-1, +1])*taxa

    def draw(self, win):
        # Desenhar os bois
        #                  cor = ( R,  G,  B)
        pygame.draw.ellipse(win, (50, 50, 50),
                            (self.x, self.y, 8, 8), 0)
        #         posicao = (x, y, largura, altura)

