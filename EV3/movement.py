#from libraries import *
from libraries import EV3Brick
#from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Direction, Stop
from verificaObstrucao import detetaBarreira
import math
from gyroscope import adjust_angle, robot, turn 

from pybricks.tools import wait

#! Inicializa os motores
# left_motor = Motor(Port.A)
# right_motor = Motor(Port.B)

forward = 550
ev3 = EV3Brick()


#robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=150)

#! Verifica se existe uma barreira a frente
def avancar():
    barreira = detetaBarreira(ev3)
    if(not barreira):
        robotStraight(forward)
    else:
        ev3.speaker.beep(400,200)
    return not barreira

def robotStraight(distancia):
    robot.straight(-distancia)





def OneBlockForward(angle, gyro_sensor):
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)
    #return avancar()
    
def OneBlocktoRight(angle, gyro_sensor):
    turn(-90)
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)
    #return avancar()
    
def OneBlocktoLeft(angle, gyro_sensor):
    turn(90)
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)
    #return avancar()

def OneBlockBehind(angle, gyro_sensor):
    turn(180)
    adjust_angle(angle, gyro_sensor)
    robotStraight(forward)
    #return avancar()
    



def test(ev3):
    #! Avanca um metro e posteriormente volta atras
    #robot.straight(1000)

    robotStraight(1000)

    ev3.speaker.beep()

    robotStraight(-1000)
    ev3.speaker.beep()

    #! Faz 360 graus e volta la posiçao inicial
    turn(360)
    ev3.speaker.beep()

    turn(-360)
    ev3.speaker.beep()