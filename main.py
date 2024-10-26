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

ev3 = EV3Brick()
hm_t = HomemTosta()

#ev3State = {"coordinates": posicao_HT, "direction": 'N'}


#test(ev3)
def main():

    print("está no ciclo\n")
    while True:

        cor = detectar_cor()
        ev3.screen.print(cor[0])

        ev3.screen.print(cor[1])
        
        # imprime_tabuleiro() 
        # hm_t.move()
        # print((hm_t.getCoordinates(),
        # hm_t.getDirection())) 
        
        wait(500)
        # if(detetaBarreira(ev3)):
        #     ev3.speaker.beep(400,1000)
            
        

#sensorUltrasonic(ev3)
main()



    

