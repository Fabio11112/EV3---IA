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
from musicas import tocar_musica_vitoria, tocar_musica_derrota



ev3 = EV3Brick()
hm_t = HomemTosta(ev3)


SEGUNDOS = 5000

#ev3State = {"coordinates": posicao_HT, "direction": 'N'}


#test(ev3)
def main():
    estava_em_torradeira = False
    pre_configuracao_cores()

    print("está no ciclo\n")
    while True:

        wait_for_button()

        cor = detectar_cor()
        rgb = cor[0]
        #ev3.screen.print(cor[0]) #rgb
        #ev3.screen.print(cor[1]) #nome da cor
        #cor_detectada = detectar_cor_por_intervalo(rgb[0], rgb[1], rgb[2])
        #ev3.screen.print("Cor: ", cor_detectada)

        #ev3.screen.print(f"Cor detectada: {cor_detectada}")
        # ev3.screen.print(f"Valores RGB: {rgb}")

        ev3.screen.print("Começa leitura")
        print("Começa leitura")
        dadosCelula = hm_t.analisaCelula()
        ev3.screen.print("Acaba leitura")
        print("Acaba leitura")


        print(dadosCelula)

        if(dadosCelula["dados"]['bolor'] == 0):
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
        #hm_t.verificaBolor(ev3)
        if(hm_t.morto):
            print("Game Over")
            
            ev3.screen.print("Game Over")
            break


        imprime_tabuleiro()

        # # dadosCelula = hm_t.analisaCelula()
        # # print(dadosCelula)


        print((hm_t.getCoordinates(),
            hm_t.getDirection())) 
        
        
        # if(detetaBarreira(ev3)):
        #     ev3.speaker.beep(400,1000)

        
        

#sensorUltrasonic(ev3)
def wait_for_button():
    while True:
        buttons = ev3.buttons.pressed()
        if Button.CENTER in buttons:
            break
        wait(100)

#main()
guardar_configuracao_cores()