from movement import OneBlockForward, OneBlocktoRight, OneBlocktoLeft, OneBlockBehind
from ia import mov_HT
from colourSensor import detectar_cor
from cores import detectar_cor_por_intervalo 
from colourSensor import detectar_cor
from movement import turn
from pybricks.tools import wait

class HomemTosta:
    
    def __init__(self):
        self.coordinates = [0,0]
        self.direction = 'N'
        self.vitoria = False
        self.morto = False
        self.distanciaBolor = 3
        

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

    def move(self):
        moveDecision = mov_HT(self.coordinates)
        
        if not moveDecision:
            return moveDecision #falso

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
        if self.direction == 'N':
            self.goForward()
        elif self.direction == 'S':
            self.goBackwards()
        elif self.direction == 'E':
            self.goLeft()
        elif self.direction == 'O':
            self.goRight()

        self.direction = 'N'
        
    def goSouth(self):
        if self.direction == 'N':
            self.goBackwards()
        elif self.direction == 'S':
            self.goForward()
        elif self.direction == 'E':
            self.goRight()
        elif self.direction == 'O':
            self.goLeft()

        self.direction = 'S'

    def goEast(self):
        if self.direction == 'N':
            self.goRight()
        elif self.direction == 'S':
            self.goLeft()
        elif self.direction == 'E':
            self.goForward()
        elif self.direction == 'O':
            self.goBackwards()

        self.direction = 'E'

    def goWest(self):
        if self.direction == 'N':
            self.goLeft()
        elif self.direction == 'S':
            self.goRight()
        elif self.direction == 'E':
            self.goBackwards()
        elif self.direction == 'O':
            self.goForward()

        self.direction == 'O'


    def goForward(self):
        OneBlockForward()

    def goRight(self):
        OneBlocktoRight()

    def goLeft(self):
        OneBlocktoLeft()

    def goBackwards(self):
        OneBlockBehind()

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
        dados = [3]*4 #valor default
        valido = False
        for _ in range(4):
            
            wait(1000)
            cor = self.verifCor()
            while not valido:
                colors = {'Preto':0, 'Azul':1, 'Vermelho':2, 'Cor Desconhecida':3}
                if(cor not in colors.keys()):
                    cor = "Cor Desconhecida"
                
                self.insereDados(dados, colors[cor])
                valido = True
            turn (-90)

        return self.decodifica(dados)  

    def decodifica(self, dados):
        bolor = 0
        torradeira = 0
        manteiga = 0

           
        bolor = dados[0]
        torradeira = dados[1]
        manteiga = (dados[2] * (1)) + (dados[3] * (4)) #4**0 = 1, 4**1 = 4

        return {'bolor': bolor, 'torradeira': torradeira, 'manteiga': manteiga}

        