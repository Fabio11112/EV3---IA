from tkinter import *
from tkinter import ttk
from random import randint
from HomemTosta import HomemTosta
from HomemTosta import Celula
import turtle

random = True

#tabuleiro inicializado com celulas vazias
tabuleiro = [[Celula() for _ in range(6)] for _ in range(6)]


def inicializaTabuleiro():
    x_mant, y_mant = 0, 0
    x_torr, y_torr = 0, 0
    n_barreiras = 0
    x_bar, y_bar = 0, 0

    if(random):

        x_mant = randint(0,5)
        y_mant = randint(0,5)

        x_torr = randint(0,5)
        y_torr = randint(0,5)  

        n_barreiras = randint(2,5)
        
    else:
        manteiga = input(f"Insira a posição da manteiga (formato x,y): ")
        x_mant, y_mant = map(int, manteiga.split(","))

        torradeira = input(f"Insira a posição da torradeira (formato x,y): ")
        x_torr, y_torr = map(int, torradeira.split(","))

        n_barreiras = input(f"Insira o número de barreiras: ")



        for i in range(int(n_barreiras)):

            barreira = ""

            if(not random):
                barreira = input(f"Insira a posição da célula da barreira (formato x,y): ")
            else:
                barreira = f"{randint(0,5)},{randint(0,5)}"

                
            x_bar, y_bar = map(int, barreira.split(","))

            barreira_dir = ""

            if(not random):
                barreira_dir = input(f"Insira a direção da barreira (Norte, Sul, Este, Oeste): ")
            else:
                opcoes = ["Norte", "Sul", "Este", "Oeste"]
                barreira_dir = opcoes[randint(0,3)] 

            
            tabuleiro[y_bar][x_bar].setBarreiras(barreira_dir)
            

        match barreira_dir:
            case "Norte":
                tabuleiro[y_bar - 1][x_bar].setBarreiras("Sul")
            case "Sul":
                tabuleiro[y_bar + 1][x_bar].setBarreiras("Norte")
            case "Este":
                tabuleiro[y_bar][x_bar + 1].setBarreiras("Oeste")
            case "Oeste":
                tabuleiro[y_bar][x_bar - 1].setBarreiras("Este")

        


    espalhaManteiga2(x_mant, y_mant)
    espalhaTorradeira(x_torr, y_torr)

    #tabuleiro[x_][y] = Celula()

# def imprimeTabuleiro(tabuleiro):
#     for y in range(len(tabuleiro)):
#         print( _________________________________________________________________ )
#         print([cel.__str__() for cel in tabuleiro[y]])
#     print( _________________________________________________________________ )    

def imprimir_tabuleiro(tablero):
    """
    Imprime el tablero de forma visual, por bloques, con distancias y barreras.
    """
    filas = len(tablero)
    columnas = len(tablero[0])

    # Generar la representación
    resultado = ""
    for i in range(filas):
        # Imprimir la fila superior de barreras
        for j in range(columnas):
            resultado += " ─ " if tablero[i][j].barreiras['Norte'] else "   "
        resultado += "\n"
        
        # Imprimir la fila principal con distancias y barreras laterales
        for j in range(columnas):
            resultado += "|" if tablero[i][j].barreiras['Oeste'] else " "
            celula = tablero[i][j]
            resultado += f"{celula.manteiga:^3}"
        resultado += "|\n" if tablero[i][-1].barreiras['Este'] else " \n"
        
        # Imprimir la fila inferior de distancias (tostadora)
        for j in range(columnas):
            resultado += "|" if tablero[i][j].barreiras['Oeste'] else " "
            celula = tablero[i][j]
            resultado += f"{celula.torradeira:^3}"
        resultado += "|\n" if tablero[i][-1].barreiras['Este'] else " \n"
        
    # Imprimir la última fila de barreras (parte inferior del tablero)
    for j in range(columnas):
        resultado += " ─ " if tablero[-1][j].barreiras['Sul'] else "   "
    resultado += "\n"

    print(resultado)
    

def espalhaTorradeira(x_torr, y_torr):

    tabuleiro[y_torr][x_torr].setTorradeira(0)

    if(y_torr + 1 < 6):
        tabuleiro[y_torr + 1][x_torr].setTorradeira(1)

    if(y_torr - 1 > -1):
        tabuleiro[y_torr - 1][x_torr].setTorradeira(1)

    if(x_torr + 1 < 6):
        tabuleiro[y_torr][x_torr + 1].setTorradeira(1)

    if(x_torr - 1 > -1):
        tabuleiro[y_torr][x_torr - 1].setTorradeira(1)





#_______________________________________________________________________________________
def espalhaManteiga2(x_mant, y_mant):
    
    for i in range(6):
        for j in range(6):
            tabuleiro[j][i].setManteiga(abs(x_mant - i) + abs(y_mant - j))


def desenha_tabuleiro(turtle, tela, tabuleiro, isTabuleiroVisitado=True, tamanho_celula=50):
    """
    Desenha o tabuleiro completo.
    """
    # Configuração inicial do Turtle
    
    

    # Dimensões do tabuleiro
    linhas = len(tabuleiro)
    colunas = len(tabuleiro[0])

    # Desenhar as células
    for i in range(linhas):
        for j in range(colunas):
        

            x = j * tamanho_celula if(isTabuleiroVisitado) else (j - 6) * tamanho_celula
            y = -i * tamanho_celula if(isTabuleiroVisitado) else (-i + 6) * tamanho_celula

            print(tabuleiro[i][j].__str__())
            tabuleiro[i][j].desenha_celula(turtle, x, y, tamanho_celula, tabuleiro[i][j])

    # Atualizar a tela
    tela.update()
    #turtle.done()


def main():
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    tela = turtle.Screen()
    tela.tracer(0)

    hm = HomemTosta(t)

    inicializaTabuleiro()
    #desenha_tabuleiro(t, tela, tabuleiro, False)

    i = 0
    hm.desenha(i)
    hm.desenhaBolor(i)
    print(hm.posicaoAtual)
    while(True):



        celulaPresente = tabuleiro[hm.posicaoAtual[1]][hm.posicaoAtual[0]]
        hm.lerCelula(celulaPresente)

        if hm.isPerdeu() or bolorChegouManteiga(hm):
            print("Perdeu!")
            break
        
        if hm.isGanhou() or bolorSeQueimou(hm):
            print("Ganhou!")
            break
        
        desenha_tabuleiro(t, tela, hm.tabuleiroExplorado)

        #desenha_tabuleiro(t, tela, tabuleiro, False)

        print(hm.posicaoAtual)
        wait = input("Pressione Enter para continuar...")

        t.reset()

        hm.mover(i)

        if(HmisInTorradeira(hm)):
            hm.moverBolor(i)
            hm.moverBolor(i)
        else:
            hm.moverBolor(i)

        i += 1

    



def HmisInTorradeira(hm):
    x = hm.posicaoAtual[0]
    y = hm.posicaoAtual[1]

    if(tabuleiro[y][x].lerTorradeira() == 0):
        print("Caíste na Torradeira")
        return True
    return False

def bolorSeQueimou(hm):
    x = hm.posicaoBolor[0]
    y = hm.posicaoBolor[1]

    if(tabuleiro[y][x].lerTorradeira() == 0):
        print("O Bolor se queimou")
        return True
    return False

def bolorChegouManteiga(hm):
    x = hm.posicaoBolor[0]
    y = hm.posicaoBolor[1]

    if(tabuleiro[y][x].lerManteiga() == 0):
        return True
    return False


main()

