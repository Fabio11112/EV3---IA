from sensorUltrasonico import sensorUltrasonic
from movement import *
from pybricks.tools import wait 

distancia_Obstrucao = 100


def detetaBarreira(ev3):
    distancia = sensorUltrasonic(ev3)
    ev3.screen.print("mm", distancia)
    return distancia < distancia_Obstrucao
