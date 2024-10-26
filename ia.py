import random


#! Definir a dimensão do tabuleiro
Tab_Dimensao = 6
posicao_BVM = [5, 5]  # Posição inicial do Bolor Verde Móvel (BVM)
##----------
posicao_Torradeira = [random.randint(0, Tab_Dimensao-1), random.randint(0, Tab_Dimensao-1)]  # Posição aleatória da Torradeira
#-----------
#tab = [posicao_HT[0]][posicao_HT[0]] 

#! Começa por criar a matriz de 6x6, vazia que vai representar o tabuleiro
tab = [[' ' for _ in range(Tab_Dimensao)] for _ in range(Tab_Dimensao)]

#tab(0, 0)
   # Coloca os elementos no tabuleiro
   
tab[posicao_Torradeira[0]][posicao_Torradeira[1]] = 'T'
#prioridades = ['N', 'S', 'E', 'O']
    
#! Definir a posição do homen tosta, no momento inicial
def imprime_tabuleiro():
    
    
    #! Imprime a Matriz
    for fila in tab:
        print(fila)
    print("\n")




def mov_HT(posicao_HT):
    #!Introduçao com movimento simpleficado
    mov = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
    newPositionChosen = False

    while  not newPositionChosen:
        escolha = random.choice(list(mov.keys()))
        nova_pos = [posicao_HT[0] + mov[escolha][0], posicao_HT[1] + mov[escolha][1]]
        #!Verifica que não saia do tabuleiro
        if 0 <= nova_pos[0] < Tab_Dimensao and 0 <= nova_pos[1] < Tab_Dimensao:
            posicao_HT[:] = nova_pos
            newPositionChosen = True
        
    print("O homem tosta moveu-se para: ")
    print(escolha)
    return [posicao_HT, escolha] #! retorna a nova posição do EV3