from movement import OneBlockForward, OneBlocktoRight, OneBlocktoLeft, OneBlockBehind
from ia import mov_HT
from colourSensor import detectar_cor
from cores import detectar_cor_por_intervalo 
from colourSensor import detectar_cor
from gyroscope import turn
from pybricks.tools import wait
from verificaObstrucao import detetaBarreira
from gyroscope import reset_angle, adjust_angle 
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port, Direction

directions = ['N', 'E', 'S', 'O']
gyro_sensor = GyroSensor(Port.S4, Direction.COUNTERCLOCKWISE)
gyro_sensor.reset_angle(90)

print("Angulo acumulado inicio: ", gyro_sensor.angle())

class HomemTosta:
    
    def __init__(self, ev3):
        self.coordinates = [0,0]
        self.direction = 'N'
        self.vitoria = False
        self.morto = False
        self.distanciaBolor = 3
        self.ev3 = ev3
        

    def verificaBolor(self, ev3):
        cor = detectar_cor()
        rgb = cor[0]
        cor_detectada = detectar_cor_por_intervalo(rgb[0], rgb[1], rgb[2])
        game = True

        ev3.screen.print("cor:", cor_detectada)

        if(cor_detectada == 'Verde'):
            print("O homem tosta tocou o bolor")
            self.morto = True

    def getCoordinates(self):
        return self.coordinates

    def setDirection(self, value):
        return self.direction

    def getDirection(self):
        return self.direction

    def move(self, barreiras):
        print("A mover")
        moveDecision = mov_HT(self.coordinates, barreiras)
        print(moveDecision)
        
        # if not moveDecision:
        #     return moveDecision #falso

        if moveDecision[1] == 'N':
            self.goNorth()
        elif moveDecision[1] == 'S':
            self.goSouth()
        elif moveDecision[1] == 'E':
            self.goEast()
        elif moveDecision[1] == 'O':
            self.goWest()

        self.direction = moveDecision[1]
        self.coordinates = moveDecision[0]
        

    def goNorth(self):
        print("Angulo acumulado em goNorth: ", gyro_sensor.angle())
        angle = 90
        if self.direction == 'N':
            self.goForward(angle)
        elif self.direction == 'S':
            self.goBackwards(angle)
        elif self.direction == 'E':
            self.goLeft(angle)
        elif self.direction == 'O':
            self.goRight(angle)

        self.direction = 'N'
        
    def goSouth(self):
        print("Angulo acumulado em goSouth: ", gyro_sensor.angle())
        angle = -90
        if self.direction == 'N':
            self.goBackwards(angle)
        elif self.direction == 'S':
            self.goForward(angle)
        elif self.direction == 'E':
            self.goRight(angle)
        elif self.direction == 'O':
            self.goLeft(angle)
        self.direction = 'S'
        

    def goEast(self):
        print("Angulo acumulado em goEast: ", gyro_sensor.angle())
        angle = 0
        if self.direction == 'N':
            self.goRight(angle)
        elif self.direction == 'S':
            self.goLeft(angle)
        elif self.direction == 'E':
            self.goForward(angle)
        elif self.direction == 'O':
            self.goBackwards(angle)

        self.direction = 'E'

        

    def goWest(self):
        print("Angulo acumulado em goWest: ", gyro_sensor.angle())
        angle = 180
        if self.direction == 'N':
            self.goLeft(angle)
        elif self.direction == 'S':
            self.goRight(angle)
        elif self.direction == 'E':
            self.goBackwards(angle)
        elif self.direction == 'O':
            self.goForward(angle)

        self.direction == 'O'

        


    def goForward(self, angle):
        #adjust_angle(angle, gyro_sensor)
        OneBlockForward(angle, gyro_sensor)

    def goRight(self, angle):
        #adjust_angle(angle, gyro_sensor)
        OneBlocktoRight(angle, gyro_sensor)

    def goLeft(self, angle):
        #adjust_angle(angle, gyro_sensor)
        OneBlocktoLeft(angle, gyro_sensor)

    def goBackwards(self, angle):
        #adjust_angle(angle, gyro_sensor)
        OneBlockBehind(angle, gyro_sensor)

    def setCoordinates(self, value):
        self.coordinates = value

    def verifCor(self):
        rgb = detectar_cor()[0]
        cor = detectar_cor_por_intervalo(rgb[0], rgb[1], rgb[2])
        print(cor)
        return cor
        
    def insereDados(self, dados, dadoLido):
        options = {"N":3,"S":1,"E":0,"O":2}
        dados[options[self.direction]] = dadoLido
        #dados.insert(options[self.direction], dadoLido)
        #[3]  manteiga;  [1]  torradeira;  [0]    bolor;  [2]  manteiga

  

    def analisaCelula(self):
        count = 0
        indice = {"N": 0, "E": 1, "S": 2, "O": 3}
        barreira = [False]*4

        direcaoInicial = indice[self.direction]

        dados = [3]*4 #valor default
        valido = False
        for _ in range(4):

            isBarreira = detetaBarreira(self.ev3)
            wait(1000)
            cor = self.verifCor()

            while not valido:
                colors = {'Preto':0, 'Azul':1, 'Vermelho':2, 'Cor Desconhecida':3}
                if(cor not in colors.keys()):
                    cor = "Cor Desconhecida"
                self.insereDados(dados, colors[cor])
                valido = True

            if(isBarreira):
                print((direcaoInicial + _) % 4)
                barreira[(direcaoInicial + _) % 4] = True
            turn (-90)

        barreiraDict = {"N": barreira[0], "E": barreira[1], "S": barreira[2], "O": barreira[3]}
        print(self.direction)
        print(barreiraDict)
        return {"dados":self.decodifica(dados), "barreira":barreiraDict}

    def decodifica(self, dados):

        print("Superior esquerdo :", )
        bolor = 0
        torradeira = 0
        manteiga = 0

           
        bolor = dados[0]
        torradeira = dados[1]
        manteiga = (dados[2] * (1)) + (dados[3] * (4)) #4**0 = 1, 4**1 = 4

        return {'bolor': bolor, 'torradeira': torradeira, 'manteiga': manteiga}

    #! def ajustaAngulo(self, targetAngle):
