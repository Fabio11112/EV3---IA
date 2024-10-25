#from libraries import *
from libraries import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from verificaObstrucao import detetaBarreira

#! Inicializa os motores
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

ev3 = EV3Brick()


robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=150)

#! Verifica se existe uma barreira a frente
def avancar():
    barreira = detetaBarreira(ev3)
    if(not barreira):
        robotStraight(400)
    else:
        ev3.speaker.beep(400,200)
    return barreira

def robotStraight(distancia):
    robot.straight(-distancia)

def turn(angle):
    robot.turn(angle*2)

def OneBlockForward():
    avancar()
    
def OneBlocktoRight():
    turn(-90)
    avancar()
    

def OneBlocktoLeft():
    turn(90)
    avancar()

def OneBlockBehind():
    turn(180)
    avancar()
    



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

 
