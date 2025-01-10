import turtle
import random

debug = False

class HomemTosta:
    def __init__(self, turtle):
        """
        __init__ - Construtor da classe HomemTosta

        :param turtle: objeto turtle para desenhar o tabuleiro
        """
        self.tamanho_celula = 50 #tamanho da célula
        self.tabuleiroExplorado = [[Celula() for _ in range(6)] for _ in range(6)]  #criação de matriz 6x6
        self.posicaoAtual = (0, 0)  #posição inicial
        self.posicaoBolor = (5, 5)  #posição do bolor
        self.celulasManteiga = [] #lista de células com manteiga
        self.celulasTorradeira = [] #lista de células com torradeira

        for i in range(6): #preenchimento da lista de células com manteiga
            for j in range(6):
                if(i == 0 and j == 0):
                    continue
                self.celulasTorradeira.append((i, j))

        self.resolverManteiga = [] #lista de células a resolver com manteiga
        self.resolverTorradeira = [] #lista de células a resolver com torradeira

        self.isResolvingButter = False #flag para resolver manteiga
        self.isResolvingToaster = False #flag para resolver torradeira

        self.t = turtle #objeto turtle para desenhar o tabuleiro
        self.t.shape("circle") #forma do objeto turtle
        self.t.color("orange") #cor do objeto turtle
        self.t.penup() #não desenhar

    
    def manteigaDescoberta(self):
        """
        manteigaDescoberta - Verifica se a manteiga foi descoberta

        :return: True se a manteiga foi descoberta, False caso contrário
        """
        return len(self.celulasManteiga) == 1

    def torradeiraDescoberta(self):
        """
        torradeiraDescoberta - Verifica se a torradeira foi descoberta

        :return: True se a torradeira foi descoberta, False caso contrário
        """
        return len(self.celulasTorradeira) == 1

    def isPerdeu(self):
        """
        isPerdeu - Verifica se o HomemTosta perdeu
        :return: True se o HomemTosta perdeu, False caso contrário
        """
        if(self.posicaoAtual == self.posicaoBolor):
            return True
        
        return False
    
    def isGanhou(self):
        """
        isGanhou - Verifica se o HomemTosta ganhou
        :return: True se o HomemTosta ganhou, False caso contrário
        """
        x = self.posicaoAtual[0]
        y = self.posicaoAtual[1]    

        if(self.tabuleiroExplorado[y][x].lerManteiga() == 0):
            return True
        return False
  
    def lerCelula(self, celula):
        """
        lerCelula - Lê a célula do tabuleiro explorado

        :param celula: tuplo com as coordenadas da célula
        :return: objeto Celula
        """
        self.tabuleiroExplorado[self.posicaoAtual[1]][self.posicaoAtual[0]] = celula    #Valores de x e y estão ao contrario
        self.tabuleiroExplorado[self.posicaoAtual[1]][self.posicaoAtual[0]].visitada = True

    def decideToResolve(self): 
        """Classe que representa o Homem Tosta no simulador.

        Esta classe gerencia o estado e o movimento do Homem Tosta, incluindo a interação com manteiga e torradeira.
        """ 
        manteiga_len = len(self.resolverManteiga)
        torradeira_len = len(self.resolverTorradeira) 

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
    
    def calculateDirection(self, passo):
        """Calcula a direção do movimento com base no passo fornecido.

        Args:
            passo (tuple): Uma tuple representando o passo ou movimento na forma (x, y).

        Returns:
            int: Um inteiro representando a direção do movimento.
                 3 para oeste, 2 para leste, 1 para norte e 0 para sul.
        """
        diferenca = (self.posicaoAtual[0] - passo[0], self.posicaoAtual[1] - passo[1])
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

    def seguintePasso(self):
        """Determina o próximo passo do Homem Tosta no simulador.

        Returns:
            tuple: Uma tuple representando o próximo passo na forma (x, y).
        """
        if(self.isResolvingButter):
            self.resolverManteiga.pop(0)
            print(self.resolverManteiga[0])
            return self.calculateDirection(self.resolverManteiga[0])
            
        elif(self.isResolvingToaster):
            self.resolverTorradeira.pop(0)
            print(self.resolverTorradeira[0])
            return self.calculateDirection(self.resolverTorradeira[0])

        else: #se tomarmos como verdade que bolor_x >= homem_tosta_x
            celula_atual = self.tabuleiroExplorado[self.posicaoAtual[1]][self.posicaoAtual[0]]

            if(self.posicaoBolor == (5,1)):
                if self.posicaoAtual == (4, 0):
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



    #Utilizador escolhe para onde se vai movimentar
    def fazerDecisao(self):
        """Permite ao Homem Tosta escolher a direção para se mover.

        Returns:
            str: Uma string representando a direção escolhida.
        """         
        while(True):
            result = 0
            decisoes = {0:"Norte", 1:"Sul", 2:"Este", 3:"Oeste"}
            if(debug):
                result = int(input(f"Insira a seguinte direção da manteiga (0:'Norte', 1:'Sul', 2:'Este', 3:'Oeste') "))
            else:
                result =  self.seguintePasso()
            return decisoes[result]
    
    #Verifica a decisao e mexe-se na posição escolhida
    def mover(self, itr):
        """Atualiza o estado do Homem Tosta com base em uma iteração fornecida.

        Args:
        itr (int): O número da iteração atual.
        """ 
        direcao = self.fazerDecisao()
        if(direcao == "Norte"):
            self.posicaoAtual = (self.posicaoAtual[0], self.posicaoAtual[1] - 1)
        elif(direcao == "Sul"):
            self.posicaoAtual = (self.posicaoAtual[0], self.posicaoAtual[1] + 1)
        elif(direcao == "Este"):
            self.posicaoAtual = (self.posicaoAtual[0] + 1, self.posicaoAtual[1])
        elif(direcao == "Oeste"):
            self.posicaoAtual = (self.posicaoAtual[0] - 1, self.posicaoAtual[1])
        self.desenha(itr)
        
    #Move o bolor consoante a posição do HomemTosta
    def moverBolor(self, itr):
        """Move o bolor com base na posição atual do Homem Tosta.
            Args:
            itr (int): O número da iteração atual.
        """
        if(self.posicaoAtual[1] - self.posicaoBolor[1]<0):
            self.posicaoBolor = (self.posicaoBolor[0], self.posicaoBolor[1] - 1)
        elif(self.posicaoAtual[1] - self.posicaoBolor[1] > 0):
            self.posicaoBolor = (self.posicaoBolor[0], self.posicaoBolor[1] + 1)
        elif(self.posicaoAtual[0] - self.posicaoBolor[0] < 0):
            self.posicaoBolor = (self.posicaoBolor[0] - 1, self.posicaoBolor[1])
        elif(self.posicaoAtual[0] - self.posicaoBolor[0] > 0):
            self.posicaoBolor = (self.posicaoBolor[0] + 1, self.posicaoBolor[1])

        self.desenhaBolor(itr)

    def desenha(self, itr):
        """Desenha o  Homem Tosta no quadro na posição atual.
            Args: 
            itr (int): O número da iteração atual.
        """
        x = self.posicaoAtual[0] * self.tamanho_celula + self.tamanho_celula / 2
        y = -self.posicaoAtual[1] * self.tamanho_celula - self.tamanho_celula / 2
        self.t.penup()
        self.t.goto(x, y)
        self.t.write(f'HM{itr}', align="center", font=("Arial", 6, "normal"))
        

    def desenhaBolor(self, itr):
        """Desenha o bolor no quadro da interação atual.
            Args:
            itr (int): O número da iteração atual."""
        x = self.posicaoBolor[0] * self.tamanho_celula + self.tamanho_celula / 2
        y = -self.posicaoBolor[1] * self.tamanho_celula - self.tamanho_celula / 2
        self.t.penup()
        self.t.goto(x, y)
        self.t.write(f'B{itr}', align="center", font=("Arial", 6, "normal"))

    def inicializaCelulasManteiga(self, dist):
        """ 
        inicializaCelulasManteiga - Inicializa as células com manteiga.
        Args:
        dist (int): A distância da manteiga em relação à posição inicial.
        """
        for i in range(6):
            for j in range(6):
                if(i + j == dist):
                    self.celulasManteiga.append((j, i))

    def atualizaCelulasManteiga(self, dist):
        """
        atualizaCelulasManteiga - Atualiza as células com manteiga.
        Args:
        dist (int): A distância da manteiga em relação à posição atual.

        """
        print(f"Posição atual: {self.posicaoAtual}")
        x = self.posicaoAtual[0]
        y = self.posicaoAtual[1]
        celulasAtualizadas = []

        for i in self.celulasManteiga:
            distancia = abs(x - i[0]) + abs(y - i[1])
            #print(f"Distância de célula {i}: {distancia}")
            if(distancia == dist):
                celulasAtualizadas.append(i)

        self.celulasManteiga = celulasAtualizadas

    def atualizaCelulasTorradeira(self, dist):
        """Atualiza as células com torradeira.
        Args:
        dist (int): A distância da torradeira em relação à posição atual.
        """
        
        around = {(0, 1), (0, -1), (1, 0), (-1, 0)}
        if dist == " ":
            for i in around:
                position = (self.posicaoAtual[0] + i[0], self.posicaoAtual[1] + i[1])
                if(position[0] < 6 and position[0] >= 0 and position[1] < 6 and position[1] >= 0):
                    x_ht, y_ht = self.posicaoAtual
                    if(position in self.celulasTorradeira):
                        self.celulasTorradeira.remove(position)
            
            if(self.posicaoAtual in self.celulasTorradeira):   
                self.celulasTorradeira.remove(self.posicaoAtual)

            return
        if dist == 1:
            i = 0
            while i < len(self.celulasTorradeira):
                x, y = self.posicaoAtual
                diferenca = abs(x - self.celulasTorradeira[i][0]) + abs(y - self.celulasTorradeira[i][1])
                print("diferenca: ", diferenca)
                print("celula: ", self.celulasTorradeira[i])
                if(diferenca != 1):
                    self.celulasTorradeira.remove(self.celulasTorradeira[i])
                else:
                    i += 1
            
            if(self.posicaoAtual in self.celulasTorradeira):   
                self.celulasTorradeira.remove(self.posicaoAtual)
            return

        if dist == 0:
            self.celulasTorradeira = [(self.posicaoAtual[0], self.posicaoAtual[1])]


            
    def mostraCelulasManteiga(self):
        """Mostra as células com manteiga."""
        print(f"Células manteiga: \n{self.celulasManteiga}")

    def mostraCelulasTorradeira(self):
        """Mostra as células com torradeira."""
        print(f"Células torradeira: \n{self.celulasTorradeira}")

    def espalhaManteiga(self, x_mant, y_mant):
        """Espalha a manteiga no tabuleiro explorado.
        Args:
        x_mant (int): A posição x da manteiga.
        y_mant (int): A posição y da manteiga.
        """
        for i in range(6):
            for j in range(6):
                self.tabuleiroExplorado[j][i].setManteiga(abs(x_mant - i) + abs(y_mant - j))

    def espalhaTorradeiraTabuleiroCompleto(self, x_torr, y_torr):
        """
        espalhaTorradeiraTabuleiroCompleto - Espalha a torradeira no tabuleiro explorado.
        Args:
        x_torr (int): A posição x da torradeira.
        y_torr (int): A posição y da torradeira.
        """
        for i in range(6):
            for j in range(6):
                self.tabuleiroExplorado[j][i].setTorradeira(abs(x_torr - i) + abs(y_torr - j))

    
class Celula:
    """
    Classe que representa uma célula no tabuleiro."""
    def __init__(self):
        """
        __init__ - Construtor da classe Celula.
        """
        self.manteiga = 0 #distância da manteiga
        self.torradeira = ' ' #distância da torradeira
        self.barreiras = {"Norte": False, "Sul": False, "Este": False, "Oeste": False} #barreiras
        self.visitada = False #flag para verificar se a célula foi visitada
    def __str__(self):
        """
        __str__ - Representação da célula em forma de string.
        Returns:
        str: Uma string representando a célula.
        """
        return f"(m: {self.manteiga}  t: {self.torradeira})\nBarreiras: {self.barreiras}"
    
    def lerManteiga(self):
        """
        lerManteiga - Lê a distância da manteiga.
        Returns:
        int: A distância da manteiga.
        """
        return self.manteiga
    
    def lerTorradeira(self):
        """
        lerTorradeira - Lê a distância da torradeira.
        Returns:
        int: A distância da torradeira.
        """
        return self.torradeira
    
    
    def setTorradeira(self, torradeira):
        """
        setTorradeira - Define a distância da torradeira.
        Args:
        torradeira (int): A distância da torradeira.
        """
        self.torradeira = torradeira
    
    def setManteiga(self, manteiga):
        """
        setManteiga - Define a distância da manteiga.
        Args:
        manteiga (int): A distância da manteiga."""
        self.manteiga = manteiga
    
    def setBarreiras(self, barr_direcao):
        """
        setBarreiras - Define as barreiras.
        Args:
        barr_direcao (str): A direção da barreira.
        """
        self.barreiras[barr_direcao] = True


    def desenha_celula(self, t, x, y, tamanho, celula):
        """
        Desenha uma célula na posição (x, y) com o tamanho especificado.
        Representa as distâncias e desenha as barreiras.
        Args:
        t (turtle.Turtle): O objeto turtle para desenhar.
        x (int): A posição x da célula.
        y (int): A posição y da célula.
        tamanho (int): O tamanho da célula.
        celula (Celula): A célula a desenhar.
        """
        # Mover para a posição inicial da célula
        t.penup() #não desenhar
        t.goto(x, y) #mover para a posição x, y
        t.pendown() #começar a desenhar

        # Desenhar as barreiras
        if celula.barreiras['Norte']:
            t.goto(x + tamanho, y)
        else:
            t.penup()
            t.goto(x + tamanho, y)
            t.pendown()
            
        if celula.barreiras['Este']:
            t.goto(x + tamanho, y - tamanho)
        else:
            t.penup()
            t.goto(x + tamanho, y - tamanho)
            t.pendown()
            
        if celula.barreiras['Sul']:
            t.goto(x, y - tamanho)
        else:
            t.penup()
            t.goto(x, y - tamanho)
            t.pendown()
            
        if celula.barreiras['Oeste']:
            t.goto(x, y)
        else:
            t.penup()
            t.goto(x, y)
            t.pendown()

        # Escrever os valores no centro da célula
        t.penup()
        t.goto(x + tamanho / 4, y - tamanho / 4)
        t.write(celula.manteiga, align="center", font=("Arial", 10, "normal"))
        t.goto(x + tamanho / 4, y - 3 * tamanho / 4)
        t.write(celula.torradeira, align="center", font=("Arial", 10, "normal"))



class Manteiga:
    """
    Classe que representa a manteiga no simulador.
    """
    def __init__(self, x, y):
        """
        __init__ - Construtor da classe Manteiga.
        Args:
        x (int): A posição x da manteiga.
        y (int): A posição y da manteiga.
        """
        self.posicao = (x, y)

    def lerPosicao(self):
        """
        lerPosicao - Lê a posição da manteiga.
        Returns:
        tuple: Uma tuple representando a posição da manteiga.
        """
        return self.posicao

    def setPosicao(self, x, y):
        """
        setPosicao - Define a posição da manteiga.
        Args:
        x (int): A posição x da manteiga.
        y (int): A posição y da manteiga.
        """

        self.posicao = (x, y)       

class Torradeira:
    """
    Classe que representa a torradeira no simulador."""
    def __init__(self, x, y):
        """
        __init__ - Construtor da classe Torradeira.
        Args:
        x (int): A posição x da torradeira.
        y (int): A posição y da torradeira.
        """
        self.posicao = (x, y)


    def lerPosicao(self):
        """
        lerPosicao - Lê a posição da torradeira.
        Returns:
        tuple: Uma tuple representando a posição da torradeira.
        """
        return self.posicao

    def setPosicao(self, x, y):
        """
        setPosicao - Define a posição da torradeira.
        Args:
        x (int): A posição x da torradeira.
        y (int): A posição y da torradeira.
        """
        self.posicao = (x, y) 