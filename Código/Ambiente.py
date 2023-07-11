import pygame
import random
import math
import numpy as np
import pandas as pd


def is_prime(number):
    # Função pra ajudar a dividir os piquetes no croqui
    divisores = []
    if number > 2:
        for i in range(2, number):
            if number % i == 0:
                divisores.append(i)
        else:
            if len(divisores) == 0:
                return None
    else:
        return 1

    return divisores[math.ceil(len(divisores)*0.5) - 1]


class Ambiente():
    def __init__(self):
        self.bois = 0
        self.piquetes = 0
        self.doy = 0
        self.croqui = None
        self.preco_piquete = 400
        self.preco_bois = 40
        self.preco_instal_irrig = 200
        self.preco_irrig = 20
        self.dinheiro = 5000
        self.lucro = 0
        self.custos_fixos = 10 # Aumentar a cada mes
        self.aumentou_cf = False # Controle do aumento dos custos
        self.soma_forragem = 0
        self.fast_forward = False

        # Dia atual do ciclo
        self.ciclo = 0
        # Dia do fim do ciclo
        self.dia_ciclo = 300
        # Ciclo acabou?
        self.final_ciclo = False

        # IMPLEMENTAR
        self.dados = pd.DataFrame(columns=["Ano", "Mes", "Dia",
                                            "Temp", "Chuva"],
                                  dtype=float)
        self.temperatura = []
        self.meses = []
        self.ano = -1
        self.mes = 0
        self.atualizou_ano = False
        self.anos = []
        # numeros 100% chutados
        self.temperatura_media = [25, 25, 25, 23, 20, 17,
                                  17, 20, 23, 25, 25, 25]
        self.chuva_media = [250, 200, 250, 100, 50, 0,
                            0, 50, 100, 200, 200, 250]
        self.chuva = []

    def calculo_diario(self, taxa):
        for _ in range(taxa):
            self.set_mes()
            self.simular_temperatura()
            self.simular_chuva()
            linha = [self.anos[-1],self.meses[-1],self.doy,
                     self.temperatura[-1],self.chuva[-1]]
            df_linha = pd.DataFrame([linha], columns = ["Ano",
                                                        "Mes",
                                                        "Dia",
                                                        "Temp",
                                                        "Chuva"])
            self.dados = self.dados._append(df_linha,
                                           ignore_index=True)

    def set_mes(self):
        # JAN
        if self.doy >= 0 and self.doy <= 31:
            self.mes = 1
            if not self.atualizou_ano:
                self.ano += 1
                self.atualizou_ano = True
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # FEV
        elif self.doy >= 32 and self.doy <= 59:
            self.mes = 2
            self.atualizou_ano = False
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # MAR
        elif self.doy >= 60 and self.doy <= 90:
            self.mes = 3
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # ABR
        elif self.doy >= 91 and self.doy <= 120:
            self.mes = 4
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # MAI
        elif self.doy >= 121 and self.doy <= 151:
            self.mes = 5
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # JUN
        elif self.doy >= 152 and self.doy <= 181:
            self.mes = 6
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # JUL
        elif self.doy >= 182 and self.doy <= 212:
            self.mes = 7
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # AGO
        elif self.doy >= 213 and self.doy <= 243:
            self.mes = 8
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # SET
        elif self.doy >= 244 and self.doy <= 273:
            self.mes = 9
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # OUT
        elif self.doy >= 274 and self.doy <= 304:
            self.mes = 10
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # NOV
        elif self.doy >= 305 and self.doy <= 334:
            self.mes = 11
            self.meses.append(self.mes)
            self.anos.append(self.ano)
        # DEZ
        elif self.doy >= 335 and self.doy <= 365:
            self.mes = 12
            self.meses.append(self.mes)
            self.anos.append(self.ano)

    def simular_temperatura(self):
        self.temperatura.append(max(0,
            random.gauss(self.temperatura_media[self.mes-1], 2)))

    def simular_chuva(self):
        self.chuva.append(max(0,
            random.gauss(self.chuva_media[self.mes-1], 100)))

    def atualizar_ciclo(self):
        # Contar os dias do ciclo
        if self.fast_forward:
            taxa = 15
        else:
            taxa = 1
        self.ciclo += taxa
        if self.ciclo >= self.dia_ciclo:
            self.final_ciclo = True
            self.ciclo = 0
        else:
            self.final_ciclo = False

    def atualizar_forragem(self, soma):
        # "Soma" é o total de forragem nos piquetes
        # To usando para descontar do salario se deixar
        # a grama no piquete sem boi, mas no modelo final vai
        # ter alguma outra coisa (morte das plantas, ...)
        self.soma_forragem = soma

    def atualizar_lucro(self, valor=0):
        self.lucro += valor

    def set_ff(self):
        self.fast_forward = not self.fast_forward

    def passar_dia(self, num_dias=1):
        if self.fast_forward and num_dias == 1:
            self.passar_dia(14)

        self.doy = (self.doy + num_dias)%365

    def receber_lucros(self):
        self.dinheiro += self.lucro
        self.lucro = 0

    def atualizar_custos_fixos(self, valor=None):
        if not self.aumentou_cf:
            if valor:
                self.custos_fixos += valor
            else:
                # PROVAVELMENTE VAI MODIFICAR
                # função do numero de piquetes, de cabeças fora
                # de piquete e da soma total de forragem
                self.custos_fixos = 10*(self.piquetes +
                                        self.bois +
                                        self.soma_forragem/100-5)
                # estabelecer um custo fixo mínimo de 10
                self.custos_fixos = max(10, self.custos_fixos)
            self.aumentou_cf = True

    def descontar_custos_fixos(self):
        self.dinheiro -= self.custos_fixos
        self.dinheiro = int(self.dinheiro)
        self.custos_fixos = 0

    def comprar_piquete(self):
        self.dinheiro -= self.preco_piquete
        self.adicionar_piquetes()

    def vender_piquete(self):
        if self.remover_piquetes():
            self.dinheiro += int(self.preco_piquete*0.8)

    def comprar_boi(self):
        self.dinheiro -= self.preco_bois
        self.adicionar_bois()

    def vender_boi(self):
        if self.remover_bois():
            self.dinheiro += int(self.preco_bois*0.8)

    def adicionar_piquetes(self):
        self.piquetes += 1
        self.get_croqui()

    def remover_piquetes(self):
        if self.piquetes > 0:
            self.piquetes -= 1
            self.get_croqui()
            return True
        self.get_croqui()
        return False

    def adicionar_bois(self):
        self.bois += 1

    def remover_bois(self):
        if self.bois > 0:
            self.bois -= 1
            return True
        return False

    def montar_croqui(self):
        n = is_prime(self.piquetes)
        if n:
            self.croqui = (int(self.piquetes/n), n)
        else:
            self.piquetes += 1
            self.montar_croqui()
            self.piquetes -= 1

    def get_croqui(self):
        self.montar_croqui()
        # print(self.croqui)
        return self.croqui


