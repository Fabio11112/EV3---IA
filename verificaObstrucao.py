from sensorUltrasonico import sensorUltrasonic
from movement import *
from pybricks.tools import wait 

distancia_Obstrucao = 100


def detetaBarreira(ev3):
    distancia = sensorUltrasonic(ev3)
    ev3.screen.print("mm", distancia)
    if  distancia < distancia_Obstrucao:
        ev3.speaker.beep(400,200)
        return True
    return False
