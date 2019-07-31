import pygame
import sys
import locale
from Boi import Boi
from Ambiente import Ambiente
from Piquete import Piquete
from Janelas import menuPrevisao, menuPiquete, telaInicial,\
                    telaPrincipal, telaGameOver, redraw_window

#TODO DEIXAR O JOGUINHO MENOS PESADO

#TODO deixar o joguinho mais bonito

#TODO menu com estatisticas gerais (temperatura, chuva)
#     menu com estatisticas do piquete (umidade do solo)

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

width = 800
height = 600
size = width, height

def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()

    pygame.mixer.music.load("../SFX/music.mp3")
    pygame.mixer.music.set_volume(0.2)

    moo = pygame.mixer.Sound("../SFX/moo.wav")
    grass = pygame.mixer.Sound("../SFX/grass.wav")
    water = pygame.mixer.Sound("../SFX/water.wav")
    coin = pygame.mixer.Sound("../SFX/coin.wav")
    kaching = pygame.mixer.Sound("../SFX/ka-ching.wav")
    click = pygame.mixer.Sound("../SFX/click.wav")
    misclick = pygame.mixer.Sound("../SFX/misclick.wav")

    passar_dia = pygame.USEREVENT + 1
    pygame.time.set_timer(passar_dia, 500)
    comecar = None
    win_inicio = pygame.display.set_mode((500, 500))
    inicio = telaInicial()


    while not comecar:
        redraw_window(win_inicio, inicio)
        pygame.display.update()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                click.play()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if inicio.botao_comecar.is_over(pos):
                    click.play()
                    comecar = True

    if not comecar:
        return

    atualizou_bois = False

    screen = pygame.display.set_mode(size)

    env = Ambiente()
    prev = menuPrevisao(env)
    prev_menu = []

    princ = telaPrincipal(env)
    bois = []
    piquetes = []
    piquetes_menus = []
    
    menu_aberto = False
    menu_prev_aberto = False

    pygame.mixer.music.play(-1)
    while True:

        if env.dinheiro < -1000 or env.dinheiro > 10000:
            # Fim do jogo
            break

        # Atualização anual
        if not menu_aberto:
            if env.final_ciclo:
                # print("Vendendo bois")
                bois_backup = bois[:]
                for b in bois_backup:
                    if b.peso >= 50:
                        for p in piquetes:
                            if b.piq == p:
                                p.remover_bois()
                                p.env.remover_bois()
                        kaching.play()
                        bois.remove(b)
                        env.atualizar_lucro(100)
                env.receber_lucros()

        # Atualização mensal
            if 15*round(env.doy/15)%30 == 0 and \
                    env.custos_fixos > 0:
                coin.play()
            if 15*round(env.doy/15)%30 == 0:
                # Cobrar custos depois do dia 15
                env.atualizar_custos_fixos()
                custo_irrig = sum(list(map(Piquete.descontar_irrig,
                                           piquetes)))
                env.atualizar_custos_fixos(custo_irrig)
                env.descontar_custos_fixos()
            else:
                if env.aumentou_cf:
                    env.aumentou_cf = False
                list(map(Piquete.resetar_preco_irrig, piquetes))

        while any(peso == 0 for peso in list(map(lambda x: x.peso,
                                                 bois))):
            # bois vão morrer
            bois_backup = bois[:]
            for b in bois_backup:
                if b.peso == 0:
                    for p in piquetes:
                        if b.piq == p:
                            p.remover_bois()
                            p.env.remover_bois()
                    moo.play()
                    bois.remove(b)


        if atualizou_bois:
            for i, b in enumerate(bois):
                b.get_antigos()

            for i, b in enumerate(bois):
                b.reset()
            atualizou_bois = False

        redraw_window(screen, princ,
                      *piquetes, *bois, *piquetes_menus,
                      *prev_menu)
        pygame.display.update()

        _ = list(map(Boi.update, bois))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                click.play()
                sys.exit()

            elif event.type == passar_dia and not menu_aberto and\
                    not menu_prev_aberto:
                # Atualização diária
                env.simular_temperatura()
                env.passar_dia()
                env.atualizar_ciclo()
                env.atualizar_forragem(sum(list(map(lambda x:
                                                        x.forragem,
                                                    piquetes))))
                list(map(Piquete.atualizar_grama, piquetes))
                list(map(Boi.atualizar_peso, bois))
                # print(list(map(lambda x: x.peso, bois)))
                list(map(Boi.atualizar_idade, bois))

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Fast forward
                if princ.botao_ff.is_over(pos) and\
                        not (menu_aberto or menu_prev_aberto):
                    click.play()
                    env.set_ff()

                # Comprar boi
                if princ.ad_bois.is_over(pos) and\
                        not (menu_aberto or menu_prev_aberto):
                    coin.play()
                    env.comprar_boi()
                    # print("Cabeças de gado: {}".format(env.bois))

                # Vender boi
                if princ.rm_bois.is_over(pos) and\
                        not (menu_aberto or menu_prev_aberto):
                    if env.bois > 0:
                        kaching.play()
                        env.vender_boi()
                    else:
                        misclick.play()
                    # print("Cabeças de gado: {}".format(env.bois))

                # Comprar piquete
                if princ.botao_ad_piquete.is_over(pos) and\
                        not (menu_aberto or menu_prev_aberto):
                    grass.play()
                    env.comprar_piquete()
                    atualizou_bois = True
                    piquetes.append(Piquete(env, len(piquetes)))

                # Vender piquete
                if princ.botao_rm_piquete.is_over(pos) and\
                        not (menu_aberto or menu_prev_aberto):
                    if env.get_croqui()[0] > 0:
                        grass.play()
                        for _ in range(piquetes[len(piquetes)-
                                                          1].bois):
                            piquetes[len(piquetes)-
                                        1].remover_bois()
                            for b in bois:
                                if b.piq == piquetes[len(piquetes)-
                                                                1]:
                                    bois.remove(b)
                        atualizou_bois = True
                        env.vender_piquete()
                        piquetes.pop()
                    else:
                        misclick.play()
                        # print("Erro")
                # print(piquetes)

                # Abrir menus
                if not menu_prev_aberto:
                    if princ.botao_prev.is_over(pos) and\
                            not menu_aberto:
                        click.play()
                        prev_menu.append(prev)
                        menu_prev_aberto = True
                    elif menu_aberto:
                        pass
                # Se o menu da previsao estiver aberto
                else:
                    if prev_menu[0].on_fechar(pos):
                        click.play()
                        prev_menu.pop()
                        menu_prev_aberto = False
                        continue

                    elif not prev_menu[0].on_menu(pos):
                        misclick.play()



                if not menu_aberto:
                    for p in piquetes:
                        if p.is_over(pos):
                            click.play()
                            piquetes_menus.append(menuPiquete(p))
                            menu_aberto = True
                # Se o menu do piquete estiver aberto
                else:
                    # Fechar menu
                    if piquetes_menus[0].on_fechar(pos) and\
                            not menu_prev_aberto:
                        click.play()
                        piquetes_menus.pop()
                        menu_aberto = False

                    elif not piquetes_menus[0].on_menu(pos):
                        misclick.play()

                    # Colocar boi no piquete
                    elif piquetes_menus[0].on_ad_bois(pos) and\
                            not menu_prev_aberto:
                        if env.bois > 0:
                            moo.play()
                            piquetes_menus[0].piq.adicionar_bois()
                            bois.append(Boi(piquetes_menus[0].piq))
                        else:
                            misclick.play()

                    # Colocar todos os bois no piquete
                    elif piquetes_menus[0].on_ad_todos(pos) and\
                            not menu_prev_aberto:
                        if env.bois > 0:
                            moo.play()
                            for _ in range(env.bois):
                                piquetes_menus[0].piq.\
                                         adicionar_bois()
                                bois.append(Boi(
                                     piquetes_menus[0].piq))
                        else:
                            misclick.play()

                    # Remover boi do piquete
                    elif piquetes_menus[0].on_rm_bois(pos) and\
                            not menu_prev_aberto:
                        if piquetes_menus[0].piq.bois > 0:
                            moo.play()
                            piquetes_menus[0].piq.remover_bois()
                            for b in bois:
                                if b.piq == piquetes_menus[0].piq:
                                    bois.remove(b)
                        else:
                            misclick.play()

                    # Remover todos os bois
                    elif piquetes_menus[0].on_rm_todos(pos) and\
                            not menu_prev_aberto:
                        if piquetes_menus[0].piq.bois > 0:
                            moo.play()
                            for _ in range(
                                    piquetes_menus[0].piq.bois):
                                piquetes_menus[0].piq.\
                                        remover_bois()
                                for b in bois:
                                    if b.piq ==\
                                            piquetes_menus[0].piq:
                                        bois.remove(b)

                        else:
                            misclick.play()

                    #Irrigar
                    elif piquetes_menus[0].on_irrigado(pos) and\
                            not menu_prev_aberto:
                        water.play()
                        piquetes_menus[0].piq.set_irrig()

    pygame.mixer.music.stop()
    
    game_over = pygame.display.set_mode((800, 250))
    tela_go = telaGameOver(env)
    resposta = None
    while resposta == None:
        redraw_window(game_over, tela_go)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                click.play()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click.play()
                if tela_go.botao_sim.is_over(pos):
                    resposta = "s"
                if tela_go.botao_nao.is_over(pos):
                    resposta = "n"

    if resposta == "s":
        main()


if __name__ == "__main__":
    main()
