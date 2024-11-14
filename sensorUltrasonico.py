from libraries import UltrasonicSensor, Port, wait
#from movement import *


def sensorUltrasonic(ev3):

    #!Crie uma instância do sensor ultrassônico conectado à Porta 3
    ultrasonic_sensor = UltrasonicSensor(Port.S3)

    #while True:
        #! Obtenha a distância em cm
    distance = ultrasonic_sensor.distance()
    return distance
        #! Amostra a distancia
        #ev3.screen.print("{} cm", distance)
        #! Apos 5 segundos repete a verificaçao
        #wait(500)