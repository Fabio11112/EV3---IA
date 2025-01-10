#from libraries import *
from libraries import EV3Brick
#from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Direction, Stop
from verificaObstrucao import detetaBarreira
import math
from gyroscope import adjust_angle, robot, turn 

from pybricks.tools import wait

forward = 560
ev3 = EV3Brick()


#! Verifica se existe uma barreira a frente
def avancar():
    """Função que verifica se existe uma barreira a frente
    e avança se não existir
    Returns:
        bool: True se não existir barreira, False se existe barreira"""
    barreira = detetaBarreira(ev3)
    if(not barreira):
        robotStraight(forward)
    else:
        ev3.speaker.beep(400,200)
    return not barreira

def robotStraight(distancia):
    """Função que faz o robot andar para a frente ou para trás
    Args:
        distancia (int): Distancia que o robot vai andar, positiva para a frente e negativa para trás"""
    robot.straight(-distancia)

def OneBlockForward(angle, gyro_sensor):
    """Função que faz o robot andar uma casa para a frente
    Args:
        angle (int): Angulo que o robot tem de ajustar
        gyro_sensor (GyroSensor): Sensor giroscópio
    """
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)

def OneBlocktoRight(angle, gyro_sensor):
    """
    Função que faz o robot andar uma casa para a direita
    Args:
        angle (int): Angulo que o robot tem de ajustar
        gyro_sensor (GyroSensor): Sensor giroscópio
    """
    turn(-90)
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)

    
def OneBlocktoLeft(angle, gyro_sensor):
    """
    Função que faz o robot andar uma casa para a esquerda
    Args:
        angle (int): Angulo que o robot tem de ajustar
        gyro_sensor (GyroSensor): Sensor giroscópio
    """
    turn(90)
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)


def OneBlockBehind(angle, gyro_sensor):
    """
    Função que faz o robot andar uma casa para trás
    Args:
        angle (int): Angulo que o robot tem de ajustar
        gyro_sensor (GyroSensor): Sensor giroscópio
    """
    turn(180)
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)
    
def test(ev3):
    """Função que testa os movimentos do robot
    Args:
        ev3 (EV3Brick): Instância do EV3Brick
    """
    robotStraight(1000)
    ev3.speaker.beep()
    robotStraight(-1000)
    ev3.speaker.beep()
    #! Faz 360 graus e volta la posiçao inicial
    turn(360)
    ev3.speaker.beep()
    turn(-360)
    ev3.speaker.beep()