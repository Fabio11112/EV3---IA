from sensorUltrasonico import sensorUltrasonic
from movement import *
from pybricks.tools import wait 

distancia_Obstrucao = 100


def detetaBarreira(ev3):
    """método que deteta uma barreira à frente do robô

    Args:
        ev3 (EV3Brick): objeto do processador EV3

    Returns:
        booleano: True se houver barreira, False caso contrário
    """
    distancia = sensorUltrasonic(ev3)
    ev3.screen.print("mm", distancia)
    if  distancia < distancia_Obstrucao:
        ev3.speaker.beep(400,200)
        return True
    return False
