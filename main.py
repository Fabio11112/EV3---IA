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

    if len(hm.celulasTorradeira) == 1:
        x = hm.bolor[0]
        y = hm.bolor[1]

        if (hm_t.tabuleiroExplorado[y][x].lerTorradeira() == 0):
            print("O Bolor se queimou")
            return True
        return False

def bolorChegouManteiga(hm):
    if(len(hm.celulasManteiga) == 1):
        x = hm.bolor[0]
        y = hm.bolor[1]

        mant_x = hm.celulasManteiga[0][0]
        mant_y = hm.celulasManteiga[0][1]

        if(x == mant_x and y == mant_y):
            return True
        
        return False

    return False #caso de incerteza


def main1():
    estava_em_torradeira = False
    pre_configuracao_cores()

    print("está no ciclo\n")
    while True:

        wait_for_button()

        cor = detectar_cor()
        rgb = cor[0]
        ev3.screen.print("Começa leitura")
        print("Começa leitura")
        dadosCelula = hm_t.analisaCelula()
        ev3.screen.print("Acaba leitura")
        print("Acaba leitura")


        print(dadosCelula)

        if(hm_t.coordinates == hm_t.bolor):
            ev3.screen.print("Game Over")
            print("Game Over")
            tocar_musica_derrota()
            break
        elif(dadosCelula["dados"]['manteiga'] == 0):
            ev3.screen.print("Victory")
            print("Victory")
            tocar_musica_vitoria()
            break
        elif(dadosCelula["dados"]["torradeira"] == 0):
            if(not estava_em_torradeira):
                estava_em_torradeira = True
                continue
            else:
                estava_em_torradeira = False



        hm_t.move(dadosCelula["barreira"])
        if(hm_t.morto):
            print("Game Over")
            
            ev3.screen.print("Game Over")
            break


        imprime_tabuleiro()
        print("Posicao bolor: ", hm_t.bolor)
        hm_t.calculaNovaPosicaoBolor()
        print("Nova posicao bolor: ", hm_t.bolor)

        print("(Coordenadas, Direção):", (hm_t.getCoordinates(),
            hm_t.getDirection())) 


def main():
    torradeiraEspalhada, manteigaEspalhada = False, False
    hmWasInToaster = False

    i = 0

    #hm_t.analisaCelula()
    #calculoDeBusca(hm_t)
    #ganhar_ou_perder = verificarPerderGanhar(hm_t)

    while True:
        #if ganhar_ou_perder != 0:
            #break~
        celulaPresente = hm_t.tabuleiroExplorado[hm_t.coordinates[1]][hm_t.coordinates[0]]
        if(not celulaPresente.visitada):
            hm_t.analisaCelula()
        #calculoDeBusca(hm_t, hmWasInToaster)

        hmIsInToaster = HmisInTorradeira(hm_t)
        print("ANTES DE SE MOVER:")
        print("HT: ", hm_t.coordinates)
        print("BVM: ", hm_t.bolor)
        print("Posições Manteiga: ", hm_t.celulasManteiga)
        print("Posições Torradeira: ", hm_t.celulasTorradeira)
        print("Árvore manteiga: ", hm_t.resolverManteiga)
        print("Árvore torradeira: ", hm_t.resolverTorradeira)

        if(not hmIsInToaster or hmWasInToaster):
            #!!!!!!!!!!!!!!!!!!!!!!!!
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

        # if(HmisInTorradeira(hm_t)):
        #     batman_melody()
        #     hm_t.moverBolor()
        #     hm_t.moverBolor()
        # else:
        #     hm_t.moverBolor()


#!------------------------------
#!------------------------------        
        wait_for_button()

        print("Buscar manteiga: ", hm_t.isResolvingButter)
        print("Buscar torradeira: ", hm_t.isResolvingToaster)

        if verificarPerderGanhar(hm_t):
            break


#!------------------------------ 
        #wait_for_button()
#!------------------------------



def calculoDeBusca(hm_t, hmWasInToaster):
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

            #!!!!!!!!!!!!!!!!!
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
    

#sensorUltrasonic(ev3)
def wait_for_button():
    while True:
        buttons = ev3.buttons.pressed()
        if Button.CENTER in buttons:
            break
        wait(100)

main()



#guardar_configuracao_cores()  #azul -> vermelho -> preto -> branco