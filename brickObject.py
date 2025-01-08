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

#print("Angulo acumulado inicio: ", gyro_sensor.angle())

# Definição da classe "HomemTosta"
class HomemTosta:
    
    def __init__(self, ev3):
        self.coordinates = (0,0)
        self.tabuleiroExplorado = [[Celula() for _ in range(6)] for _ in range(6)]
        self.direction = 'N'

        #estes não são usados no simulador, logo verificar se são usados a seguir
        ######
        self.vitoria = False
        self.morto = False
        self.distanciaBolor = 3
        ######


        self.ev3 = ev3
        self.bolor = (5, 5)
        self.celulasManteiga = []
        self.celulasTorradeira = []

        for i in range(6):
            for j in range(6):
                if(i == 0 and j == 0):
                    continue
                self.celulasTorradeira.append((i, j))

        self.resolverManteiga = []
        self.resolverTorradeira = []

        self.isResolvingButter = False
        self.isResolvingToaster = False
        


    # def verificaBolor(self, ev3):
    #     cor = detectar_cor()
    #     rgb = cor[0]
    #     cor_detectada = detectar_cor_por_intervalo(rgb[0], rgb[1], rgb[2])
    #     game = True

    #     ev3.screen.print("cor:", cor_detectada)

    #     if(cor_detectada == 'Verde'):
    #         print("O homem tosta tocou o bolor")
    #         self.morto = True

    def getCoordinates(self):
        return self.coordinates

    # def setDirection(self, value):
    #     return self.direction

    def getDirection(self):
        return self.direction


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

    # def setCoordinates(self, value):
    #     self.coordinates = value

    def verifCor(self):
        rgb = detectar_cor()[0]
        cor = detectar_cor_por_intervalo(rgb[0], rgb[1], rgb[2])
        #print(cor)
        return cor
        
#faz a decisão de movimento e move o homem tosta
    def move(self):
        print("A mover")
        #moveDecision = mov_HT(self.coordinates, barreiras)

        #!MUDANÇA #!MUDANÇA #!MUDANÇA #!MUDANÇA #!MUDANÇA #!MUDANÇA #!MUDANÇA #!MUDANÇAS
        moveDecision = self.fazerDecisao()
    
        if moveDecision == 'Norte':
            self.goNorth()
            self.direction = 'N'
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 1)
        elif moveDecision == 'Sul':
            self.goSouth()
            self.direction = 'S'
            self.coordinates = (self.coordinates[0], self.coordinates[1] + 1)
        elif moveDecision == 'Este':
            self.goEast()
            self.direction = 'E'
            self.coordinates = (self.coordinates[0] + 1, self.coordinates[1])
        elif moveDecision == 'Oeste':
            self.goWest()
            self.direction = 'O'
            self.coordinates = (self.coordinates[0] - 1, self.coordinates[1])
        else:
            print("Erro na decisão de movimento:", moveDecision)

        # self.direction = moveDecision[1]
        # self.coordinates = moveDecision[0]
        
#!insere os novos dados obtidos da nova célula

    #insere os dados obtidos dentro do array "dados" na posição correta
    def insereDados(self, dados, dadoLido, direcao):
        
        options = (1,2,0)


        #[M0, M1, T]

        #print(direcao)
        dados[options[direcao]] = dadoLido
        
        #dados.insert(options[self.direction], dadoLido)
        #[3]  manteiga;  [1]  torradeira;  [0]    bolor;  [2]  manteiga

#método que analisa a célula e atualiza o tabuleiro explorado com as novas informações
    def analisaCelula(self):
        count = 0
        indice = {"N": 0, "E": 1, "S": 2, "O": 3}
        barreira = [False]*4
        print("Sentido do robô: ", self.direction)
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


        #Atualiza os dados das barreiras encontrada
        barreiraDict = {"Norte": barreira[0], "Este": barreira[1], "Sul": barreira[2], "Oeste": barreira[3]}

        for i in barreiraDict:
            if barreiraDict[i]:
                self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]].setBarreiras(i)
                if(i == "Norte" and self.coordinates[1] - 1 >= 0):
                    self.tabuleiroExplorado[self.coordinates[1]-1][self.coordinates[0]].setBarreiras("Sul")
                elif(i == "Sul" and self.coordinates[1] + 1 >= 0):
                    self.tabuleiroExplorado[self.coordinates[1]+1][self.coordinates[0]].setBarreiras("Norte")
                elif(i == "Este" and self.coordinates[0] + 1 < 0):
                    self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]+1].setBarreiras("Oeste")
                elif(i == "Oeste" and self.coordinates[0] - 1 >= 0):
                    self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]-1].setBarreiras("Este")


        self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]].visitada = True

        dadosDecodificados = self.decodifica(dados)
        print("Dados decodificados: ", dadosDecodificados)

        self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]].setManteiga(dadosDecodificados['manteiga'])


        #se torradeira for igual a 3, quer dizer que não está perto
        #2 nunca deve dar, valor inexistente para a torradeira
        if(dadosDecodificados['torradeira'] < 2):
            self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]].setTorradeira(dadosDecodificados['torradeira'])

            
        return {"dados":self.decodifica(dados), "barreira":barreiraDict}


    def decodifica(self, dados):

        #!print("Superior esquerdo :", )
        #bolor = 0
        torradeira = 0
        manteiga = 0

           
        torradeira = dados[2]
        manteiga = (dados[0] * (1)) + (dados[1] * (4)) #4**0 = 1, 4**1 = 4

        return {'torradeira': torradeira, 'manteiga': manteiga}

    
    def calculaNovabolor(self):
        diferenca = [self.bolor[0] - self.coordinates[0], self.bolor[1] - self.coordinates[1]]

        if (diferenca[1] > 0):  #o bolor vai para o norte
            self.bolor = [self.bolor[0], self.bolor[1] - 1]
        elif (diferenca[1] < 0): #o bolor vai para o sul
            self.bolor = [self.bolor[0], self.bolor[1] + 1]
        elif (diferenca[0] < 0): #o bolor vai para este
            self.bolor = [self.bolor[0] + 1, self.bolor[1]]
        elif (diferenca[0] > 0):  #o bolor vai para oeste
            self.bolor = [self.bolor[0] - 1, self.bolor[1]]

#!____________________________________________________________________________________

#!PARTE DE HOMEM-TOSTA
    #calcula a seguinte direção que o homem tosta deve tomar
    def calculateDirection(self, passo):
        diferenca = (self.coordinates[0] - passo[0], self.coordinates[1] - passo[1])
        if(diferenca[0] == 1):
            #oeste
            return 3
        elif(diferenca[0] == -1):
            #este
            return 2
        elif(diferenca[1] == 1):
            #norte
            return 0
        elif(diferenca[1] == -1):
            #sul
            return 1

    #calcula o próximo passo que o homem tosta deve tomar
    def seguintePasso(self):
        if(self.isResolvingButter):
            self.resolverManteiga.pop(0)
            print(self.resolverManteiga[0])
            return self.calculateDirection(self.resolverManteiga[0])
            
        elif(self.isResolvingToaster):
            self.resolverTorradeira.pop(0)
            print(self.resolverTorradeira[0])
            return self.calculateDirection(self.resolverTorradeira[0])

        else: #se tomarmos como verdade que bolor_x >= homem_tosta_x
            celula_atual = self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]]

            if(self.bolor == (5,1)):
                if self.coordinates == (4, 0):
                    #oeste
                    return 3

            celula_4_0 = self.tabuleiroExplorado[0][4]
            celula_3_1 = self.tabuleiroExplorado[1][3]

            if(celula_4_0.visitada or celula_3_1.visitada):
                
                if(celula_atual.barreiras['Sul']):
                    #oeste
                    return 3
                #sul
                return 1

            if(celula_atual.barreiras['Este']):
                #sul
                return 1
            else:
                #este
                return 2

    #decide se deve resolver a manteiga ou a torradeira ou nenhum
    def decideToResolve(self):
        manteiga_len = len(self.resolverManteiga)
        torradeira_len = len(self.resolverTorradeira) 

        
        print("manteiga_len: ", manteiga_len)
        print("torradeira_len: ", torradeira_len)

        if(torradeira_len > 0):
            if(manteiga_len == 0 or torradeira_len < manteiga_len):
                self.isResolvingToaster = True
                self.isResolvingButter = False
            else:
                self.isResolvingButter = True
                self.isResolvingToaster = False
        else:
            if(manteiga_len != 0):
                self.isResolvingButter = True
                self.isResolvingToaster = False


        print("Novo isResolvingButter: ", self.isResolvingButter)
        print("Novo isResolvingToaster: ", self.isResolvingToaster)

    #retorna True se a manteiga foi descoberta
    def manteigaDescoberta(self):
            return len(self.celulasManteiga) == 1

    #retorna True se a torradeira foi descoberta
    def torradeiraDescoberta(self):
        return len(self.celulasTorradeira) == 1

    #retorna True se o BVM toca o HT
    def isPerdeu(self):
        if(self.coordinates == self.bolor):
            return True
        
        return False

    #retorna True se o HT toca a manteiga
    def isGanhou(self):
        if(len(self.celulasManteiga) == 1):
            x = self.coordinates[0]
            y = self.coordinates[1]    

            if(self.tabuleiroExplorado[y][x].lerManteiga() == 0):
                return True
            return False

    def fazerDecisao(self):        
        while(True):
            result = 0
            decisoes = {0:"Norte", 1:"Sul", 2:"Este", 3:"Oeste"}

            result =  self.seguintePasso()
            # if(self.coordinates[1] == 0 and result == 0 or
            #    self.coordinates[1] == 5 and result == 1 or
            #    self.coordinates[0] == 0 and result == 3 or
            #    self.coordinates[0] == 5 and result == 2):
            #     continue
            return decisoes[result]

    #move o bolor
    def moverBolor(self):
        if(self.coordinates[1] - self.bolor[1]<0):
            self.bolor = (self.bolor[0], self.bolor[1] - 1)
        elif(self.coordinates[1] - self.bolor[1] > 0):
            self.bolor = (self.bolor[0], self.bolor[1] + 1)
        elif(self.coordinates[0] - self.bolor[0] < 0):
            self.bolor = (self.bolor[0] - 1, self.bolor[1])
        elif(self.coordinates[0] - self.bolor[0] > 0):
            self.bolor = (self.bolor[0] + 1, self.bolor[1])

        #self.desenhaBolor(itr)


    #inicializa o array de celulas de manteiga
    def inicializaCelulasManteiga(self, dist):
        for i in range(6):
            for j in range(6):
                if(i + j == dist):
                    self.celulasManteiga.append((j, i))

    #atualiza as células possíveis para a manteiga
    def atualizaCelulasManteiga(self, dist):
        #print("Posição atual:",self.coordinates)
        x = self.coordinates[0]
        y = self.coordinates[1]
        celulasAtualizadas = []

        for i in self.celulasManteiga:
            distancia = abs(x - i[0]) + abs(y - i[1])
            #print(f"Distância de célula {i}: {distancia}")
            if(distancia == dist):
                celulasAtualizadas.append(i)

        self.celulasManteiga = celulasAtualizadas

    #atualiza as células possíveis para a torradeira
    # def atualizaCelulasTorradeira(self, dist):

    #     if(len(self.celulasTorradeira) == 1):
    #         return

        
    #     celulaPresente = self.tabuleiroExplorado[self.coordinates[1]][self.coordinates[0]]
    #     if(celulaPresente.lerTorradeira() == 0):
    #         self.celulasTorradeira = [(self.coordinates[0], self.coordinates[1])]
    #         return

    #     if dist == ' ':
    #         if (len(self.celulasTorradeira) > 1 and self.coordinates in self.celulasTorradeira):
    #             self.celulasTorradeira.remove(self.coordinates)

    #         i = 0

    #         while i < len(self.celulasTorradeira):
    #             moves = [(0,-1), (0, 1), (1, 0), (-1, 0)]
    #             j = 0
    #             while j < len(moves):
    #                 print("i", i)
    #                 print("len", len(self.celulasTorradeira))
    #                 movement = (self.celulasTorradeira[i][0] + moves[j][0], self.celulasTorradeira[i][1] + moves[j][1])
    #                 if(movement[0] > 5 or movement[0] < 0 or movement[1] > 5 or movement[1] < 0):
    #                     continue

    #                 celula = self.tabuleiroExplorado[movement[1]][movement[0]]
    #                 print("Visitada (", movement[0], ", ", movement[1], ")?: ", celula.visitada)
    #                 print("torradeira 0?: ", celula.lerTorradeira())
    #                 if(celula.visitada and celula.lerTorradeira() == ' '):
    #                     self.celulasTorradeira.remove(self.celulasTorradeira[i])
    #                     break
    #                 elif(j == len(moves) - 1):
    #                     i += 1

    #                 j += 1

    #         return 

        
    #     x = self.coordinates[0]
    #     y = self.coordinates[1]

    #     newCelulasTorradeira = []

    #     if x + 1 < 6 and self.tabuleiroExplorado[y][x + 1].lerManteiga() == 0:
    #         newCelulasTorradeira.append((x + 1, y))
    #     if x - 1 >= 0 and self.tabuleiroExplorado[y][x - 1].lerManteiga() == 0:
    #         newCelulasTorradeira.append((x - 1, y))
    #     if y + 1 < 6 and self.tabuleiroExplorado[y + 1][x].lerManteiga() == 0:
    #         newCelulasTorradeira.append((x, y + 1))
    #     if y - 1 >= 0 and self.tabuleiroExplorado[y - 1][x].lerManteiga() == 0:
    #         newCelulasTorradeira.append((x, y - 1))


    #     if self.celulasTorradeira != []:
    #         self.celulasTorradeira = list(set(self.celulasTorradeira) & set(newCelulasTorradeira))
    #         return
            
    #     self.celulasTorradeira = newCelulasTorradeira

    def atualizaCelulasTorradeira(self, dist):
        around = {(0, 1), (0, -1), (1, 0), (-1, 0)}
        if dist == " ":
            for i in around:
                position = (self.coordinates[0] + i[0], self.coordinates[1] + i[1])
                if(position[0] < 6 and position[0] >= 0 and position[1] < 6 and position[1] >= 0):
                    x_ht, y_ht = self.coordinates
                    if(position in self.celulasTorradeira):
                        self.celulasTorradeira.remove(position)
            
            if(self.coordinates in self.celulasTorradeira):   
                self.celulasTorradeira.remove(self.coordinates)

            return
            

        if dist == 1:
            i = 0
            while i < len(self.celulasTorradeira):
                x, y = self.coordinates
                diferenca = abs(x - self.celulasTorradeira[i][0]) + abs(y - self.celulasTorradeira[i][1])
                print("diferenca: ", diferenca)
                print("celula: ", self.celulasTorradeira[i])
                if(diferenca != 1):
                    self.celulasTorradeira.remove(self.celulasTorradeira[i])
                else:
                    i += 1
            
            if(self.coordinates in self.celulasTorradeira):   
                self.celulasTorradeira.remove(self.coordinates)
            return

        if dist == 0:
            self.celulasTorradeira = [(self.coordinates[0], self.coordinates[1])]


    def mostraCelulasManteiga(self):
        print("Células manteiga: \n", self.celulasManteiga)

    def mostraCelulasTorradeira(self):
        print("Células torradeira: \n",self.celulasTorradeira)

    def espalhaManteiga(self, x_mant, y_mant):
        for i in range(6):
            for j in range(6):
                self.tabuleiroExplorado[j][i].setManteiga(abs(x_mant - i) + abs(y_mant - j))

    def espalhaTorradeiraTabuleiroCompleto(self, x_torr, y_torr):
        for i in range(6):
            for j in range(6):
                self.tabuleiroExplorado[j][i].setTorradeira(abs(x_torr - i) + abs(y_torr - j))

                
class Celula:

    def __init__(self):
        self.manteiga = 0
        self.torradeira = ' '
        self.barreiras = {"Norte": False, "Sul": False, "Este": False, "Oeste": False}
        self.visitada = False

    # def __init__(self, manteiga, torradeira):
    #     self.manteiga = manteiga
    #     self.torradeira = torradeira
    #     self.barreiras = {"Norte": False, "Sul": False, "Este": False, "Oeste": False}

    def __str__(self):
        return "(m:" + str(self.manteiga) + " t: " + str(self.torradeira) + "\nBarreiras: " + str(self.barreiras) + ")"
    
    def lerManteiga(self):
        return self.manteiga
    
    def lerTorradeira(self):
        return self.torradeira
    
    
    def setTorradeira(self, torradeira):
        self.torradeira = torradeira
    
    def setManteiga(self, manteiga):
        self.manteiga = manteiga
    
    def setBarreiras(self, barr_direcao):
        self.barreiras[barr_direcao] = True

    
    
    
    
    
    #! def ajustaAngulo(self, targetAngle):
