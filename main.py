#!/usr/bin/env pybricks-micropython
from libraries import EV3Brick
from sensorUltrasonico import *
from movement import *
from ia import imprime_tabuleiro, mov_HT
from brickObject import HomemTosta
from sensorUltrasonico import sensorUltrasonic
from verificaObstrucao import detetaBarreira
from pybricks.tools import wait
from colourSensor import detectar_cor
from pybricks.parameters import Color
from cores import detectar_cor_por_intervalo
from pybricks.parameters import Button


ev3 = EV3Brick()
hm_t = HomemTosta()

SEGUNDOS = 5000

#ev3State = {"coordinates": posicao_HT, "direction": 'N'}


#test(ev3)
def main():

    print("está no ciclo\n")
    while True:

        cor = detectar_cor()
        rgb = cor[0]
        #ev3.screen.print(cor[0]) #rgb
        #ev3.screen.print(cor[1]) #nome da cor
        #cor_detectada = detectar_cor_por_intervalo(rgb[0], rgb[1], rgb[2])
        #ev3.screen.print("Cor: ", cor_detectada)

        #ev3.screen.print(f"Cor detectada: {cor_detectada}")
        # ev3.screen.print(f"Valores RGB: {rgb}")

        imprime_tabuleiro()

        dadosCelula = hm_t.analisaCelula()
        print(dadosCelula)


        # # # hm_t.move()
        # # # hm_t.verificaBolor(ev3)
        # # # if(hm_t.morto):
        # # #     print("Game Over")
        # # #     ev3.screen.print("Game Over")
        # # #     break


        # # # print((hm_t.getCoordinates(),
        # # # hm_t.getDirection())) 
        
        # # # analisaCelula(hm_t)



        # if(detetaBarreira(ev3)):
        #     ev3.speaker.beep(400,1000)

        wait_for_button()
        

#sensorUltrasonic(ev3)
def wait_for_button():
    while True:
        buttons = ev3.buttons.pressed()
        if Button.CENTER in buttons:
            break
        wait(100)


main()





    

