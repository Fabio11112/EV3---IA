import turtle
import random

debug = True

class HomemTosta:
    def __init__(self, turtle):
        self.tamanho_celula = 50
        self.tabuleiroExplorado = [[Celula() for _ in range(6)] for _ in range(6)]  #criação de matriz 6x6
        self.posicaoAtual = (0, 0)  #posição inicial
        self.posicaoBolor = (5, 5)  

        self.t = turtle
        self.t.shape("circle")
        self.t.color("orange")
        self.t.penup()

    ##fabio é gay ass: copilot
    def lerCelula(self, celula):
        self.tabuleiroExplorado[self.posicaoAtual[1]][self.posicaoAtual[0]] = celula    #Valores de x e y estão ao contrario

    def fazerDecisao(self):        
        while(True):
            result = 0
            decisoes = {0:"Norte", 1:"Sul", 2:"Este", 3:"Oeste"}
            if(debug):
                result = int(input(f"Insira a seguinte direção da manteiga (0:'Norte', 1:'Sul', 2:'Este', 3:'Oeste') "))
            else:
                result =  random.randint(0, 3)
            if(self.posicaoAtual[1] == 0 and result == 0 or
               self.posicaoAtual[1] == 5 and result == 1 or
               self.posicaoAtual[0] == 0 and result == 3 or
               self.posicaoAtual[0] == 5 and result == 2):
                continue

            return decisoes[result]
        
    def mover(self, itr):
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
        
    def moverBolor(self, itr):
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
        """Draw ToastMan on the board at the current position."""
        x = self.posicaoAtual[0] * self.tamanho_celula + self.tamanho_celula / 2
        y = -self.posicaoAtual[1] * self.tamanho_celula - self.tamanho_celula / 2
        self.t.penup()
        self.t.goto(x, y)
        self.t.write(f'HM{itr}', align="center", font=("Arial", 6, "normal"))
        

    def desenhaBolor(self, itr):
        """Draw ToastMan on the board at the current position."""
        x = self.posicaoBolor[0] * self.tamanho_celula + self.tamanho_celula / 2
        y = -self.posicaoBolor[1] * self.tamanho_celula - self.tamanho_celula / 2
        self.t.penup()
        self.t.goto(x, y)
        self.t.write(f'B{itr}', align="center", font=("Arial", 6, "normal"))

        



class Celula:

    def __init__(self):
        self.manteiga = 0
        self.torradeira = ' '
        self.barreiras = {"Norte": False, "Sul": False, "Este": False, "Oeste": False}

    # def __init__(self, manteiga, torradeira):
    #     self.manteiga = manteiga
    #     self.torradeira = torradeira
    #     self.barreiras = {"Norte": False, "Sul": False, "Este": False, "Oeste": False}

    def __str__(self):
        return f"(m: {self.manteiga}  t: {self.torradeira})\nBarreiras: {self.barreiras}"
    
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


    def desenha_celula(self, t, x, y, tamanho, celula):
        """
        Desenha uma célula na posição (x, y) com o tamanho especificado.
        Representa as distâncias e desenha as barreiras.
        """
        # Mover para a posição inicial da célula
        t.penup()
        t.goto(x, y)
        t.pendown()

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

    def __init__(self, x, y):
        self.posicao = (x, y)

    def lerPosicao(self):
        return self.posicao

    def setPosicao(self, x, y):
        self.posicao = (x, y)       

class Torradeira:

    def __init__(self, x, y):
        self.posicao = (x, y)


    def lerPosicao(self):
        return self.posicao

    def setPosicao(self, x, y):
        self.posicao = (x, y)         
