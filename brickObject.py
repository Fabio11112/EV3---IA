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

# Definição da classe "HomemTosta"
class HomemTosta:
    
    def __init__(self, ev3):
        self.coordinates = [0,0]
        self.direction = 'N'
        self.vitoria = False
        self.morto = False
        self.distanciaBolor = 3
        self.ev3 = ev3
        self.bolor = [2, 2]
        

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
        #!print(moveDecision)
        
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
        #!print("Angulo acumulado em goNorth: ", gyro_sensor.angle())
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
        #!print("Angulo acumulado em goSouth: ", gyro_sensor.angle())
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
        #!print("Angulo acumulado em goEast: ", gyro_sensor.angle())
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
        #!print("Angulo acumulado em goWest: ", gyro_sensor.angle())
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
        #print(cor)
        return cor
        
    def insereDados(self, dados, dadoLido, direcao):
        
        options = (1,2,0)


        #[M0, M1, T]

        print(direcao)
        dados[options[direcao]] = dadoLido
        
        #dados.insert(options[self.direction], dadoLido)
        #[3]  manteiga;  [1]  torradeira;  [0]    bolor;  [2]  manteiga

    def analisaCelula(self):
        count = 0
        indice = {"N": 0, "E": 1, "S": 2, "O": 3}
        barreira = [False]*4
        print("Direcao: ", self.direction)
        direcaoInicial = indice[self.direction]

        #dados = [3]*4 #valor default
        dados = [3]*3 #valor default
        
        
        for _ in range(4):
            valido = False

            indiceDirecao = (direcaoInicial + _) % 4

            isBarreira = detetaBarreira(self.ev3)
            wait(1000)
            
            
            
            if(isBarreira):
                #!print(indiceDirecao)
                barreira[indiceDirecao] = True
                

            if(indiceDirecao == 1): 
                print("Bolor")
                
            else:
                cor = self.verifCor()

                #!print("Cor analisada em insereDados:", cor)

                while not valido:
                    colors = {'Preto':0, 'Azul':1, 'Vermelho':2, 'Cor Desconhecida':3}
                    if(cor not in colors.keys()):
                        cor = "Cor Desconhecida"
                    
                    indiceDirecao = (0 if indiceDirecao == 0 else indiceDirecao-1)

                    #!print(indiceDirecao)

                    print("valor de cor: ", colors[cor])
                    self.insereDados(dados, colors[cor], indiceDirecao)
                    valido = True


            turn (-90)
        print("Dados captados: ", dados)

        barreiraDict = {"N": barreira[0], "E": barreira[1], "S": barreira[2], "O": barreira[3]}

        print(self.direction)
        print(barreiraDict)
        return {"dados":self.decodifica(dados), "barreira":barreiraDict}

    def decodifica(self, dados):

        #!print("Superior esquerdo :", )
        #bolor = 0
        torradeira = 0
        manteiga = 0

           
        torradeira = dados[2]
        manteiga = (dados[0] * (1)) + (dados[1] * (4)) #4**0 = 1, 4**1 = 4

        return {'torradeira': torradeira, 'manteiga': manteiga}

    
    def calculaNovaPosicaoBolor(self):
        diferenca = [self.bolor[0] - self.coordinates[0], self.bolor[1] - self.coordinates[1]]

        if (diferenca[1] > 0):  #o bolor vai para o norte
            self.bolor = [self.bolor[0], self.bolor[1] - 1]
        elif (diferenca[1] < 0): #o bolor vai para o sul
            self.bolor = [self.bolor[0], self.bolor[1] + 1]
        elif (diferenca[0] < 0): #o bolor vai para este
            self.bolor = [self.bolor[0] + 1, self.bolor[1]]
        elif (diferenca[0] > 0):  #o bolor vai para oeste
            self.bolor = [self.bolor[0] - 1, self.bolor[1]]


    
    
    
    
    
    #! def ajustaAngulo(self, targetAngle):
