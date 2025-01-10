#!/usr/bin/env pybricks-micropython
from libraries import EV3Brick
from sensorUltrasonico import *
from movement import *
from ia import imprime_tabuleiro, mov_HT
from brickObject import HomemTosta
from sensorUltrasonico import sensorUltrasonic
from verificaObstrucao import detetaBarreira
from pybricks.tools import wait
from colourSensor import detectar_cor, guardar_configuracao_cores
from pybricks.parameters import Color
from cores import detectar_cor_por_intervalo, pre_configuracao_cores
from pybricks.parameters import Button
from gyroscope import reset_angle, adjust_angle
from musicas import tocar_musica_vitoria, tocar_musica_derrota, batman_melody

from algoritmoIA import a_star_search



ev3 = EV3Brick()
hm_t = HomemTosta(ev3)
inicializada = False


SEGUNDOS = 5000


def HmisInTorradeira(hm):
    """
    Função que verifica se o Homem Tosta está numa torradeira
    Args:
        hm (HomemTosta): Homem Tosta
    Returns:
        bool: True se está numa torradeira, False caso contrário"""
    x = hm.coordinates[0]
    y = hm.coordinates[1]
    print("Coordenadas HT: ", (x, y))
    print("Valor torradeira lerTorradeir(): ", hm_t.tabuleiroExplorado[y][x].lerTorradeira())
    print("Valor torradeira torradeira: ", hm_t.tabuleiroExplorado[y][x].torradeira)
    print("Está na torradeira?: ", hm_t.tabuleiroExplorado[y][x].lerTorradeira() == 0)
    if(hm_t.tabuleiroExplorado[y][x].lerTorradeira() == 0):
        print("Caíste na Torradeira!")
        return True
    return False

def bolorSeQueimou(hm):
    """
    Função que verifica se o bolor se queimou
    Args:
        hm (HomemTosta): Homem Tosta
    Returns:
        bool: True se o bolor se queimou, False caso contrário"""
    if len(hm.celulasTorradeira) == 1:
        x = hm.bolor[0]
        y = hm.bolor[1]
        if (hm_t.tabuleiroExplorado[y][x].lerTorradeira() == 0):
            print("O Bolor se queimou")
            return True
        return False

def bolorChegouManteiga(hm):
    """
    Função que verifica se o bolor chegou à manteiga
    Args:
        hm (HomemTosta): Homem Tosta
    Returns:
        bool: True se o bolor chegou à manteiga, False caso contrário"""
    if(len(hm.celulasManteiga) == 1):
        x = hm.bolor[0]
        y = hm.bolor[1]
        mant_x = hm.celulasManteiga[0][0]
        mant_y = hm.celulasManteiga[0][1]
        if(x == mant_x and y == mant_y):
            return True
        return False
    return False #caso de incerteza

def main():
    """
    Função principal que executa o jogo"""
    hmWasInToaster = False
    while True:
        celulaPresente = hm_t.tabuleiroExplorado[hm_t.coordinates[1]][hm_t.coordinates[0]]
        if(not celulaPresente.visitada):
            hm_t.analisaCelula()
        if verificarPerderGanhar(hm_t):
            break
        hmIsInToaster = HmisInTorradeira(hm_t)
        print("ANTES DE SE MOVER:")
        print("HT: ", hm_t.coordinates)
        print("BVM: ", hm_t.bolor)
        print("Posições Manteiga: ", hm_t.celulasManteiga)
        print("Posições Torradeira: ", hm_t.celulasTorradeira)
        print("Árvore manteiga: ", hm_t.resolverManteiga)
        print("Árvore torradeira: ", hm_t.resolverTorradeira)
        if(not hmIsInToaster or hmWasInToaster):
            calculoDeBusca(hm_t, hmWasInToaster)
            hm_t.move()
            hm_t.moverBolor()
            hmWasInToaster = False
        else:
            hm_t.moverBolor()
            batman_melody() 
            hmWasInToaster = True
        print("DEPOIS DE SE MOVER:")
        print("HT: ", hm_t.coordinates)
        print("BVM: ", hm_t.bolor)
        print("Posições Manteiga: ", hm_t.celulasManteiga)
        print("Posições Torradeira: ", hm_t.celulasTorradeira)
        print("Árvore manteiga: ", hm_t.resolverManteiga)
        print("Árvore torradeira: ", hm_t.resolverTorradeira)     
        wait_for_button()
        print("Buscar manteiga: ", hm_t.isResolvingButter)
        print("Buscar torradeira: ", hm_t.isResolvingToaster)
        if verificarPerderGanhar(hm_t):
            break
def calculoDeBusca(hm_t, hmWasInToaster):
    """
    Calcula a busca a ser realizada pelo Homem Tosta
    Args:
        hm_t (HomemTosta): Homem Tosta
        hmWasInToaster (bool): True se o Homem Tosta estava numa torradeira, False caso
        contrário
    Returns:
        None
    """
    global inicializada
    celulaPresente = hm_t.tabuleiroExplorado[hm_t.coordinates[1]][hm_t.coordinates[0]]
    if inicializada:
        if not hm_t.manteigaDescoberta():
            numberButterBeforeUpdating = len(hm_t.celulasManteiga)
            hm_t.atualizaCelulasManteiga(celulaPresente.lerManteiga())
            hm_t.mostraCelulasManteiga()

            if(hm_t.torradeiraDescoberta() and numberButterBeforeUpdating != 0 and numberButterBeforeUpdating > len(hm_t.celulasManteiga)):
                hm_t.resolverTorradeira = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasTorradeira[0], hm_t.bolor, True, hm_t.celulasManteiga)
                hm_t.decideToResolve()

            if(hm_t.manteigaDescoberta()):
                celula = hm_t.celulasManteiga[0]
                hm_t.espalhaManteiga(celula[0], celula[1])

                hm_t.resolverManteiga = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasManteiga[0], hm_t.bolor)
                hm_t.decideToResolve()

                if(hm_t.torradeiraDescoberta()):
                    hm_t.resolverTorradeira = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasTorradeira[0], hm_t.bolor, True, hm_t.celulasManteiga)
                    hm_t.decideToResolve()
        else:
            if(True in celulaPresente.barreiras.values()):
                hm_t.resolverManteiga = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasManteiga[0], hm_t.bolor)
                hm_t.decideToResolve()

            elif(hmWasInToaster):
                hm_t.resolverManteiga = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasManteiga[0], hm_t.bolor)
                hm_t.decideToResolve()

        if(not hm_t.torradeiraDescoberta()):
            hm_t.atualizaCelulasTorradeira(celulaPresente.lerTorradeira())
            hm_t.mostraCelulasTorradeira()

            if(hm_t.torradeiraDescoberta()):
                celula = hm_t.celulasTorradeira[0]
                hm_t.espalhaTorradeiraTabuleiroCompleto(celula[0], celula[1])
                hm_t.resolverTorradeira = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasTorradeira[0], hm_t.bolor, True, hm_t.celulasManteiga)
                hm_t.decideToResolve()
        else:
            #e que uma nova barreira haja sido descoberta, é necessário atualizar a árvore de pesquisa
            if(True in celulaPresente.barreiras.values() and not celulaPresente.visitada):
                hm_t.resolverTorradeira = a_star_search(hm_t.tabuleiroExplorado, hm_t.coordinates, hm_t.celulasTorradeira[0], hm_t.bolor, True, hm_t.celulasManteiga)
                hm_t.decideToResolve()
    else:  
        hm_t.inicializaCelulasManteiga(celulaPresente.lerManteiga())
        hm_t.mostraCelulasManteiga()
        inicializada = True

def verificarPerderGanhar(hm_t):
    """
    Verifica se o Homem Tosta ganhou ou perdeu
    Args:
        hm_t (HomemTosta): Homem Tosta
    Returns:
        bool: True se o Homem Tosta ganhou ou perdeu, False caso contrário
    """
    if hm_t.isGanhou(): 
        print("HT chegou à Manteiga")
        tocar_musica_vitoria()
        return True
    if hm_t.isPerdeu():
        print("O Bolor chegou ao HT")
        tocar_musica_derrota()
        return True
    if(bolorChegouManteiga(hm_t)):
        print("O Bolor chegou à Manteiga")
        tocar_musica_derrota()
        return True
    if bolorSeQueimou(hm_t):
        print("O Bolor se queimou")
        tocar_musica_vitoria()
        return True
    return False

def wait_for_button():
    """
    Espera que o botão central seja pressionado
    Args:
        None
    Returns:
        None
    """
    while True:
        buttons = ev3.buttons.pressed()
        if Button.CENTER in buttons:
            break
        wait(100)

#Função principal
main()

#Este método é utilizado para guardar as configurações das cores do sensor de cor
#guardar_configuracao_cores()  #azul -> vermelho -> preto -> branco