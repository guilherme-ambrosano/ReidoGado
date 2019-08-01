import pygame
import datetime
import pandas as pd
from Grafico import fazer_grafico

class Botao():

    def __init__(self, x, y, width, height, text = "",
                 color = (100, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
    
    def draw(self, win):

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width,
                                           self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 -
                                               text.get_width()/2),
                            self.y + (self.height/2 -
                                             text.get_height()/2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class menuPrevisao:
    def __init__(self, ambiente):
        self.env = ambiente
        self.width = 630
        self.height = 330
        self.x = 85
        self.y = 85
        self.variavel = "temperatura"

    def retornar_df(self):
        df = self.env.dados
        ultimo_ano = df["Ano"].max()
        if self.env.piquetes > 0:
            df_temp = df.groupby(["Ano", "Mes"],
                                 as_index = False)["Temp"].mean()
            df_chuva = df.groupby(["Ano", "Mes"],
                                  as_index = False)["Chuva"].sum()
            df = pd.merge(df_temp, df_chuva, on=["Ano", "Mes"])
            return df
        else:
            df_temp = df.groupby(["Ano", "Mes"],
                                 as_index = False)["Temp"].mean()
            df_chuva = df_temp.copy().rename(columns = {"Ano": "Ano",\
                    "Mes": "Mes", "Temp": "Chuva"})
            df_chuva["Chuva"] = 0
            df = pd.merge(df_temp, df_chuva, on=["Ano", "Mes"])
            df.loc[0] = [0, 0, 0, 0]
            return df

    def retornar_df_old(self):
        if self.variavel == "temperatura":
            dados = self.env.temperatura
        tempo = self.env.mes
        anos = self.env.anos

        dic_dados = {
                "ano": anos,
                "tempo": tempo,
                "dados": dados}

        df = pd.DataFrame.from_dict(dic_dados)
        ultimo_ano = df["ano"].max()

        df = df.groupby(["ano", "tempo"], as_index = False).mean()
        # df.reset_index()
        # df.columns = ["ano", "tempo", "dados"]

        n_dados = df.shape[0]

        if n_dados%12 < 10 and n_dados%12 > 3:
            df = df[df.ano == ultimo_ano]
            df = df.tail(4)
            df.drop(columns = "ano", inplace = True)

            dados_medios = self.env.temperatura_media[\
                    n_dados%12:n_dados%12+3] 
            tempos_medios = range(n_dados%12, n_dados%12+3)

            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)

            df = df.append(df_medios)

        elif n_dados%12 == 1:
            if n_dados > 1:
                df = df.tail(4)
            else:
                df = df.tail(1)
                dados_inicio = self.env.temperatura_media[-3:]
                tempos_inicio = [9, 10, 11]
                dic_inicio = {
                        "ano": ultimo_ano,
                        "tempo": tempos_inicio,
                        "dados": dados_inicio}
                df_inicio = pd.DataFrame.from_dict(dic_inicio)
                df = df_inicio.append(df)

            df = df[df.ano == ultimo_ano]
            df.drop(columns = "ano", inplace = True)

            dados_medios = self.env.temperatura_media[1:4]
            tempos_medios = range(1, 4)
            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)
            df = df.append(df_medios)

        elif n_dados%12 == 2:

            if n_dados > 2:
                df = df.tail(4)
            else:
                df = df.tail(2)
                dados_inicio = self.env.temperatura_media[-2:]
                tempos_inicio = [10, 11]
                dic_inicio = {
                        "ano": ultimo_ano,
                        "tempo": tempos_inicio,
                        "dados": dados_inicio}
                df_inicio = pd.DataFrame.from_dict(dic_inicio)
            df = df[df.ano == ultimo_ano]
            df.drop(columns = "ano", inplace = True)
            dados_medios = self.env.temperatura_media[2:5]
            tempos_medios = range(2, 5)
            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)
            df = df.append(df_medios)
        elif n_dados%12 == 3:
            if n_dados > 3:
                df = df.tail(4)
            else:
                df = df.tail(3)
                dados_inicio = self.env.temperatura_media[-1]
                tempos_inicio = [11]
                dic_inicio = {
                        "ano": ultimo_ano,
                        "tempo": tempos_inicio,
                        "dados": dados_inicio}
                df_inicio = pd.DataFrame.from_dict(dic_inicio)
            df = df[df.ano == ultimo_ano]
            df.drop(columns = "ano", inplace = True)
            dados_medios = self.env.temperatura_media[3:6]
            tempos_medios = range(3, 6)
            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)
            df = df.append(df_medios)

        elif n_dados%12 == 10:
            df = df.tail(4)
            dados_medios = self.env.temperatura_media[10:]
            dados_medios.append(self.env.temperatura_media[0])
            tempos_medios = [10, 11, 0]
            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)
            df = df.append(df_medios)
        elif n_dados%12 == 11:
            df = df.tail(4)
            dados_medios = (self.env.temperatura_media[11])
            dados_medios.extend(self.env.temperatura_media[:2])
            tempos_medios = [11, 0, 1]
            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)
            df = df.append(df_medios)
        elif n_dados%12 == 12:
            df = df.tail(4)
            dados_medios = self.env.temperatura_media[:3]
            tempos_medios = [0, 1, 2]
            dic_medios = {
                    "tempo": tempos_medios,
                    "dados": dados_medios}
            df_medios = pd.DataFrame.from_dict(dic_medios)
            df = df.append(df_medios)

        return df


    def draw(self, win):
        df = self.retornar_df()
        fazer_grafico(df)

        pygame.draw.rect(win, (100, 100, 100),
                         (self.x, self.y,
                          self.width, self.height), 0)

        grafico = pygame.image.load("grafico.png")

        self.botao_fechar = Botao(655, 95, 50, 50, "X",
                                  color = (150, 150, 150))
        self.botao_fechar.draw(win)

        win.blit(grafico, (self.x+10,self.y+10))
        pygame.display.flip()

    def on_fechar(self, pos):
        if self.botao_fechar:
            return self.botao_fechar.is_over(pos)
        return None

    def on_menu(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class menuPiquete:

    def __init__(self, piquete):
        self.piq = piquete
        self.botao_ad_bois = None
        self.botao_rm_bois = None
        self.botao_fechar = None

    def set_irrig(self):
        self.piq.set_irrig()

    def adicionar_bois(self):
        self.piq.adicionar_bois()

    def remover_bois(self):
        self.piq.remover_bois()

    def draw(self, win):
        self.width = 630
        self.height = 330
        self.x = 85
        self.y = 85

        pygame.draw.rect(win, (0, 104, 55),
                         (self.x, self.y,
                          self.width, self.height), 0)

        font = pygame.font.SysFont("comicsans", 60)

        #rect(janela, cor = (R, G, B), (x, y, largura, altura), 0)
        pygame.draw.rect(win, (35, 132, 67),
                         (100, 175, 325, 175), 0)

        text_bois = font.render(str(self.piq.bois),
                                   1, (0, 0, 0))

        win.blit(text_bois, (280 + (100 - text_bois.get_width()/2),
                             175 + (175/2 -
                                    text_bois.get_height()/2)))

        #Botao(x, y, largura, altura, texto, cor = (R, G, B))
        self.botao_ad_bois = Botao(125, 200, 50, 50, "+1",
                                   color = (120, 198, 121))
        self.botao_ad_bois.draw(win)

        self.botao_ad_todos = Botao(195, 200, 150, 50, "+Todos",
                                    color = (120, 198, 121))
        self.botao_ad_todos.draw(win)

        self.botao_rm_bois = Botao(125, 270, 50, 50, "-1",
                                   color = (120, 198, 121))
        self.botao_rm_bois.draw(win)

        self.botao_rm_todos = Botao(195, 270, 150, 50, "-Todos",
                                    color = (120, 198, 121))
        self.botao_rm_todos.draw(win)

        self.botao_fechar = Botao(655, 95, 50, 50, "X",
                                  color = (120, 198, 121))
        self.botao_fechar.draw(win)

        if not self.piq.irrigado:
            self.botao_irrig = Botao(480, 250, 150, 50, "Irrigar", 
                                     color = (120, 198, 121))
        else:
            self.botao_irrig = Botao(470, 250, 225, 50,
                                     "Não irrigar",
                                     color = (120, 198, 121))
        self.botao_irrig.draw(win)


    def on_menu(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def on_fechar(self, pos):
        if self.botao_fechar:
            return self.botao_fechar.is_over(pos)
        return None

    def on_ad_bois(self, pos):
        if self.botao_ad_bois:
            return self.botao_ad_bois.is_over(pos)
        return None

    def on_ad_todos(self, pos):
        if self.botao_ad_todos:
            return self.botao_ad_todos.is_over(pos)
        return None

    def on_irrigado(self, pos):
        if self.botao_irrig:
            return self.botao_irrig.is_over(pos)
        return None

    def on_rm_bois(self, pos):
        if self.botao_rm_bois:
            return self.botao_rm_bois.is_over(pos)
        return None

    def on_rm_todos(self, pos):
        if self.botao_rm_todos:
            return self.botao_rm_todos.is_over(pos)
        return None


class telaInicial():
    def __init__(self):
        pass

    def draw(self, win):
        background = pygame.image.load("../Sprites/Ambiente/"
                                       "background2.png")
        win.blit(background, (0, -100))
        self.botao_comecar = Botao(125, 225, 250, 60, "Começar")
        self.botao_comecar.draw(win)


class telaPrincipal():
    def __init__(self, ambiente):
        self.env = ambiente
    
    def draw(self, win):
        background = pygame.image.load("../Sprites/Ambiente/"
                                       "background.png")
        win.blit(background, (0, 0))

        font = pygame.font.SysFont("comicsans", 60)
        # fast forward
        if self.env.fast_forward:
            text_ff = ">"
        else:
            text_ff = ">>"
        self.botao_ff = Botao(660, 500, 60, 60, text_ff,
                              color = (223, 194, 125))

        font = pygame.font.SysFont("comicsans", 40)
        # data
        dia_str = datetime.datetime(2018, 1, 1) +\
                datetime.timedelta(self.env.doy-1)

        text_doy = font.render("Dia : "+dia_str.strftime("%d/%b"),
                               1, (0, 0, 0))
        win.blit(text_doy, (520, 30))

        # pontuacao
        text_dinheiro = font.render("$" + str(self.env.dinheiro),
                                    1, (0, 0, 0))
        win.blit(text_dinheiro, (75, 30))

        # previsao do tempo
        self.botao_prev = Botao(740, 10, 50, 50, "P",
                                color = (100, 100, 100))

        # Gado
        #rect(janela, cor = (R, G, B), (x, y, largura, altura), 0)
        pygame.draw.rect(win, (223, 194, 125),
                         (370, 460, 245, 130), 0)

        font = pygame.font.SysFont("comicsans", 40)
        text_ad_bois = font.render("-$" + str(self.env.preco_bois),
                                   1, (215, 48, 39))
        #                             (  R,  G,  B)
        win.blit(text_ad_bois, (380, 482))
        #                      (  x,   y)

        text_rm_bois = font.render("+$"+
                                 str(int(self.env.preco_bois*0.8)),
                                   1, (26, 152, 80))
        win.blit(text_rm_bois, (380, 542))

        font = pygame.font.SysFont("comicsans", 60)
        text_bois = font.render(str(self.env.bois), 1, (0, 0, 0))
        win.blit(text_bois, (555, 505))

        font = pygame.font.SysFont("comicsans", 60)
        text_bois = font.render("Cabeças", 1, (0, 0, 0))
        win.blit(text_bois, (400, 425))

        #Botao(x, y, largura, altura, texto, cor = (R, G, B))
        self.ad_bois = Botao(470, 470, 60, 50, "+1",
                             color = (191, 129, 45))
        self.rm_bois = Botao(470, 530, 60, 50, "-1",
                             color = (191, 129, 45))

        # Piquetes
        font = pygame.font.SysFont("comicsans", 40)
        pygame.draw.rect(win, (223, 194, 125),
                         (75, 460, 245, 130), 0)

        text_ad_piquete = font.render("-$" +
                                      str(self.env.preco_piquete),
                                      1, (215, 48, 39))
        win.blit(text_ad_piquete, (85, 482))

        text_rm_piquete = font.render("+$" +
                              str(int(self.env.preco_piquete*0.8)),
                                      1, (26, 152, 80))
        win.blit(text_rm_piquete, (85, 542))

        font = pygame.font.SysFont("comicsans", 60)
        text_piquete = font.render(str(self.env.piquetes),
                                   1, (0, 0, 0))
        win.blit(text_piquete, (270, 505))

        font = pygame.font.SysFont("comicsans", 60)
        text_piquetes = font.render("Piquetes", 1, (0, 0, 0))
        win.blit(text_piquetes, (115, 425))

        self.botao_ad_piquete = Botao(190, 470, 60, 50, "+1",
                                      color = (191, 129, 45))
        self.botao_rm_piquete = Botao(190, 530, 60, 50, "-1",
                                      color = (191, 129, 45))

        self.ad_bois.draw(win)
        self.rm_bois.draw(win)
        self.botao_ad_piquete.draw(win)
        self.botao_rm_piquete.draw(win)
        self.botao_ff.draw(win)
        self.botao_prev.draw(win)


def redraw_window(screen, *args):
    #           (  R,   G,   B)
    screen.fill((255, 255, 255))
    # Depois eu to desenhando as sprites por cima da tela branca
    for item in args:
        item.draw(screen)


class telaGameOver():

    def __init__(self, ambiente):
        self.env = ambiente

    def draw(self, win):
        background = pygame.image.load("../Sprites/Ambiente/"
                                       "background2.png")
        win.blit(background, (0, -225))
 
        font = pygame.font.SysFont("comicsans", 60)
        if self.env.dinheiro < 0:
            text = font.render("Você perdeu.", 1, (0, 0, 0))
        elif self.env.dinheiro > 0:
            text = font.render("Você ganhou!", 1, (0, 0, 0))

        pontuacao = font.render("Sua pontuação: {0}${1},00"
                                "".format(
                                    "-" if self.env.dinheiro < 0\
                                            else "",
                                    abs(self.env.dinheiro)), 1, 
                                (0, 0, 0))

        continuar = font.render("Continuar?", 1, (0, 0, 0))

        win.blit(text, ((800/2 - text.get_width()/2), 15))
        win.blit(pontuacao, ((800/2 - pontuacao.get_width()/2),
                              60))
        win.blit(continuar, ((800/2 - continuar.get_width()/2),
                              105))

        self.botao_sim = Botao(50, 160, 85, 50, "Sim")
        self.botao_sim.draw(win)

        self.botao_nao = Botao(650, 160, 85, 50, "Não")
        self.botao_nao.draw(win)


