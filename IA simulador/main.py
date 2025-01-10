from tkinter import *
from tkinter import ttk
from random import randint
from HomemTosta import HomemTosta
from HomemTosta import Celula
from algoritmoIA import a_star_search
import turtle

random = False

#tabuleiro inicializado com celulas vazias
tabuleiro = [[Celula() for _ in range(6)] for _ in range(6)]


def inicializaTabuleiro():
    """inicializa o tabuleiro com as posições da manteiga, torradeira e barreiras"""
    x_mant, y_mant = 0, 0
    x_torr, y_torr = 0, 0
    n_barreiras = 0
    x_bar, y_bar = 0, 0

    if(random):

        while True:                             #Evita escolher a posição da manteiga no bolor nem no hm
            x_mant = randint(0,5)
            y_mant = randint(0,5)
            if not ((x_mant == 5 and y_mant == 5) or (x_mant == 0 and y_mant == 0)):
                break


        while True:                             #Evita escolher a posição da torradeira no bolor nem no hm nem na manteiga
            x_torr = randint(0,5)
            y_torr = randint(0,5)
            if not ((x_torr == 5 and y_torr == 5) or (x_torr == 0 and y_torr == 0) or (x_torr == x_mant and y_torr == y_mant)):
                break


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
                if(y_bar - 1 > -1):
                    tabuleiro[y_bar - 1][x_bar].setBarreiras("Sul")
            case "Sul":
                if(y_bar + 1 < 6):
                    tabuleiro[y_bar + 1][x_bar].setBarreiras("Norte")
            case "Este":
                if(x_bar + 1 < 6):
                    tabuleiro[y_bar][x_bar + 1].setBarreiras("Oeste")
            case "Oeste":
                if(x_bar - 1 > -1):
                    tabuleiro[y_bar][x_bar - 1].setBarreiras("Este")

        


    espalhaManteiga(x_mant, y_mant)
    espalhaTorradeira(x_torr, y_torr)

    
def imprimir_tabuleiro(tablero):
    """
    Imprime el tablero de forma visual, por bloques, con distancias y barreras.
    Args:
        tablero (list): Tablero a imprimir.

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
    """espalha a torradeira pelas células adjacentes
    Args:
        x_torr (int): coordenada x da torradeira
        y_torr (int): coordenada y da torradeira
    """
    tabuleiro[y_torr][x_torr].setTorradeira(0)

    if(y_torr + 1 < 6):
        tabuleiro[y_torr + 1][x_torr].setTorradeira(1)

    if(y_torr - 1 > -1):
        tabuleiro[y_torr - 1][x_torr].setTorradeira(1)

    if(x_torr + 1 < 6):
        tabuleiro[y_torr][x_torr + 1].setTorradeira(1)

    if(x_torr - 1 > -1):
        tabuleiro[y_torr][x_torr - 1].setTorradeira(1)


def espalhaManteiga(x_mant, y_mant):
    """espalha a manteiga pelas células adjacentes
    Args:
        x_mant (int): coordenada x da manteiga
        y_mant (int): coordenada y da manteiga
    """
    for i in range(6):
        for j in range(6):
            tabuleiro[j][i].setManteiga(abs(x_mant - i) + abs(y_mant - j))

def espalhaTorradeiraTabuleiroCompleto(x_torr, y_torr):
    for i in range(6):
        for j in range(6):
            tabuleiro[j][i].setTorradeira(abs(x_torr - i) + abs(y_torr - j))


def desenha_tabuleiro(turtle, tela, tabuleiro, isTabuleiroVisitado=True, tamanho_celula=50):
    """
    Desenha o tabuleiro completo.
    Args:
        turtle (Turtle): Objeto Turtle para desenhar.
        tela (Screen): Objeto Screen para atualizar a tela.
        tabuleiro (list): Tabuleiro a desenhar.
        isTabuleiroVisitado (bool): Se o tabuleiro a desenhar é o visitado ou não.
        tamanho_celula (int): Tamanho da célula a desenhar.
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

            #print(tabuleiro[i][j].__str__())
            tabuleiro[i][j].desenha_celula(turtle, x, y, tamanho_celula, tabuleiro[i][j])

    # Atualizar a tela
    tela.update()
    #turtle.done()


def main():
    """Função principal do programa."""
    torradeiraEspalhada, manteigaEspalhada = False, False

    # Configuração inicial do Turtle
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    tela = turtle.Screen()
    tela.tracer(0)

    # Inicializa o HomemTosta
    hm = HomemTosta(t)

    # Inicializa o tabuleiro
    inicializaTabuleiro()
    #desenha_tabuleiro(t, tela, tabuleiro, False)

    i = 0
    hm.desenha(i)
    hm.desenhaBolor(i)
    print(hm.posicaoAtual)
    inicializada = False
    hmWasInTorradeira = False

    while(True):
        celulaPresente = tabuleiro[hm.posicaoAtual[1]][hm.posicaoAtual[0]]
        hm.lerCelula(celulaPresente)
        
        if(inicializada):
            # manteiga no início da análise ainda sem descobrir
            if(not hm.manteigaDescoberta()):
                numberButterBeforeUpdating = len(hm.celulasManteiga)

                hm.atualizaCelulasManteiga(celulaPresente.lerManteiga())
                hm.mostraCelulasManteiga()

                # caso em que a torradeira já foi descoberta e se minimizam as células candidatas a ter a manteiga
                # é necessário atualizar a árvore de pesquisa
                if(hm.torradeiraDescoberta() and numberButterBeforeUpdating != 0 and numberButterBeforeUpdating > len(hm.celulasManteiga)):
                    hm.resolverTorradeira = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasTorradeira[0], hm.posicaoBolor, True, hm.celulasManteiga)
                    hm.decideToResolve()

                # caso em que nesta iteração da análise foi, de facto, encontrada a localização da manteiga
                if(hm.manteigaDescoberta()):
                    celula = hm.celulasManteiga[0]
                    hm.espalhaManteiga(celula[0], celula[1])

                    # faz a busca da manteiga
                    hm.resolverManteiga = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasManteiga[0], hm.posicaoBolor)
                    hm.decideToResolve()

                    # atualizar busca da torradeira se esta já tinha sido descoberta
                    if(hm.torradeiraDescoberta()):
                        hm.resolverTorradeira = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasTorradeira[0], hm.posicaoBolor, True, hm.celulasManteiga)
                        hm.decideToResolve()

            # caso em que a manteiga já foi descoberta
            else:
                # e que uma nova barreira haja sido descoberta, é necessário atualizar a árvore de pesquisa
                if(True in celulaPresente.barreiras.values()):
                    hm.resolverManteiga = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasManteiga[0], hm.posicaoBolor)
                    hm.decideToResolve()

                if(hmWasInTorradeira):
                    hm.resolverManteiga = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasManteiga[0], hm.posicaoBolor)
                    hm.decideToResolve()

            # torradeira no início da análise ainda sem descobrir
            if(not hm.torradeiraDescoberta()):
                hm.atualizaCelulasTorradeira(celulaPresente.lerTorradeira())
                hm.mostraCelulasTorradeira()

                # caso em que nesta iteração da análise seja descoberta a torradeira
                if(hm.torradeiraDescoberta()):
                    celula = hm.celulasTorradeira[0]
                    hm.espalhaTorradeiraTabuleiroCompleto(celula[0], celula[1])
                    hm.resolverTorradeira = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasTorradeira[0], hm.posicaoBolor, True, hm.celulasManteiga)
                    hm.decideToResolve()
            # torradeira já tinha sido encontrada
            else:
                # e que uma nova barreira haja sido descoberta, é necessário atualizar a árvore de pesquisa
                if(True in celulaPresente.barreiras.values() and not celulaPresente.visitada):
                    hm.resolverTorradeira = a_star_search(hm.tabuleiroExplorado, hm.posicaoAtual, hm.celulasTorradeira[0], hm.posicaoBolor, True, hm.celulasManteiga)
                    hm.decideToResolve()

        else:  # not inicializada
            hm.inicializaCelulasManteiga(celulaPresente.lerManteiga())
            hm.mostraCelulasManteiga()
            inicializada = True

        # Verifica condições de vitória ou derrota
        if hm.isGanhou(): 
            print("HT chegou à Manteiga")
            break
        if hm.isPerdeu():
            print("O Bolor chegou ao HT")
            break
        if(bolorChegouManteiga(hm)):
            print("O Bolor chegou à Manteiga")
            break
        if bolorSeQueimou(hm):
            print("O Bolor se queimou")
            break
        
        desenha_tabuleiro(t, tela, hm.tabuleiroExplorado)

        #desenha_tabuleiro(t, tela, tabuleiro, False)

        # Espera pelo usuário para continuar
        wait = input("Pressione Enter para continuar...")

        t.reset()

        # Move o HomemTosta
        hm.mover(i)

        # Move o bolor
        if(HmisInTorradeira(hm)):
            hm.moverBolor(i)
            hm.moverBolor(i)
            hmWasInTorradeira = True
        else:
            hm.moverBolor(i)
            hmWasInTorradeira = False

        i += 1


def HmisInTorradeira(hm):
    """Verifica se o HomemTosta está na torradeira
    Args:
        hm (HomemTosta): HomemTosta a verificar"""
    x = hm.posicaoAtual[0]
    y = hm.posicaoAtual[1]

    if(tabuleiro[y][x].lerTorradeira() == 0):
        print("Caíste na Torradeira")
        return True
    return False

def bolorSeQueimou(hm):
    """Verifica se o bolor se queimou
    Args:
        hm (HomemTosta): HomemTosta a verificar"""
    x = hm.posicaoBolor[0]
    y = hm.posicaoBolor[1]

    if (tabuleiro[y][x].lerTorradeira() == 0):
        print("O Bolor se queimou")
        return True
    return False

def bolorChegouManteiga(hm):
    """Verifica se o bolor chegou à manteiga
    Args:
        hm (HomemTosta): HomemTosta a verificar"""
    x = hm.posicaoBolor[0]
    y = hm.posicaoBolor[1]

    if(tabuleiro[y][x].lerManteiga() == 0):
        return True
    return False


main()
