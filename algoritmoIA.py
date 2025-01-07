import math
import heapq

COL = ROW = 6
numberStates = 0

class Cell:
    def __init__(self):
        self.pai = None
        #f = g + h
        self.f = float('inf')
        #custo total
        self.g = float('inf')
        #heuristica
        self.h = float('inf')

def is_valid(row, col, manteigaCells, bvm):
    isValid = (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

    homemTostaLost = (row == bvm[0] and col == bvm[1])

    if(len(manteigaCells) == 1):
        manteiga = manteigaCells[0]
        #se chegou à manteiga antes do que o BVM, ganhou, casó contrário, ou seja, ele não caiu na manteiga na mesma jogada
        #tudo depende de se ele caiu no BVM ou de se o BVM irá cair no Homem Tosta
        homemTostaLost = False if (row == manteiga[0] and col == manteiga[1]) else homemTostaLost

    #Verdadeiro se for uma jogada válida e se o Homem Tosta NÃO perdeu
    return isValid and not homemTostaLost


"Uma célula é não bloqueada quando não tem barreiras na direção que se deseja ir OU não esteja o bolor na posição na que se quer ir"	
def is_unblocked(grid, x_before, y_before, x_next, y_next, x_bolor, y_bolor): 
    cell_before = grid[y_before][x_before]

    x_difference = x_before - x_next
    y_difference = y_before - y_next

    # if(x_next == x_bolor and y_next == y_bolor):
    #     return False

    if(x_difference < 0 and cell_before.barreiras['Este']):
        return False
    elif(x_difference > 0 and cell_before.barreiras['Oeste']):
        return False
    elif(y_difference < 0 and cell_before.barreiras['Sul']):
        return False
    elif(y_difference > 0 and cell_before.barreiras['Norte']):
        return False

    return True

def is_destination(x, y, dest, isKillingBvm = False, bvm = None):
    if(isKillingBvm):
        return bvm[0] == dest[0] and bvm[1] == dest[1]
    return x == dest[0] and y == dest[1]


"Método que retorna a heurística da busca A* e também a seguinte posição do bolor de acordo com a posição atual"
def calculate_h_value(x, y, x_bolor, y_bolor, dest, celula):
    h_butter = abs(x - dest[0]) + abs(y - dest[1])
    butter_pos = dest
    penalty_bvm = 0
    penalty_bvm_butter = 0
    #visited_penalty = 0

    bvm_next_x, bvm_next_y = calculate_BVM_next_position(x, y, x_bolor, y_bolor)

    # if(celula.visitada):
    #     visited_penalty = 10
    
    distance_to_bvm = abs(x - bvm_next_x) + abs(y - bvm_next_y)
    if distance_to_bvm == 0:
        penalty_bvm += 1000  # Direct collision
    elif distance_to_bvm == 1:
        penalty_bvm += 20  # High risk

    # Penalty for BVM being near Butter
    distance_bvm_butter = abs(bvm_next_x - butter_pos[0]) + abs(bvm_next_y - butter_pos[1])
    
    if distance_bvm_butter == 0:
        penalty_bvm_butter += 1000  # BVM on Butter (critical)
    elif distance_bvm_butter == 1:
        penalty_bvm_butter += 50  # BVM adjacent to Butter

    #print(f"h_butter: {h_butter}, \npenalty_bvm: {penalty_bvm}, \npenalty_bvm_butter: {penalty_bvm_butter}")

    return (h_butter + penalty_bvm + penalty_bvm_butter, (bvm_next_x, bvm_next_y))

def calculate_h_value_torradeira(x, y, x_bolor, y_bolor, manteiga, dest, celula):
    #h_butter = abs(x - manteiga[0]) + abs(y - manteiga[1])
    toaster_pos = dest
    penalty_bvm = 0
    penalty_bvm_butter = 0

    bvm_next_x, bvm_next_y = calculate_BVM_next_position(x, y, x_bolor, y_bolor)

    #se o homem tosta estiver na torradeira, é mais um movimento para o BVM
    if(x == dest[0] and y == dest[1]):
        bvm_next_x, bvm_next_y = calculate_BVM_next_position(x, y, bvm_next_x, bvm_next_y)

    h_toaster = abs(bvm_next_x - toaster_pos[0]) + abs(bvm_next_y - toaster_pos[1])

    
    distance_to_bvm = abs(x - bvm_next_x) + abs(y - bvm_next_y)
    if distance_to_bvm == 0:
        penalty_bvm += 1000  # Direct collision

    # Penalty for BVM being near Butter
    distance_bvm_butter = 0
    for manteigaCell in manteiga:
        distance_bvm_butter = abs(bvm_next_x - manteigaCell[0]) + abs(bvm_next_y - manteigaCell[1])

        if distance_bvm_butter == 0:
            penalty_bvm_butter += 1000  # BVM on Butter (critical)
        elif distance_bvm_butter == 1:
            penalty_bvm_butter += 50  # BVM adjacent to Butter

    penalty_bvm_butter /= len(manteiga)
    
    return (h_toaster + penalty_bvm + penalty_bvm_butter, (bvm_next_x, bvm_next_y))


def calculate_BVM_next_position(x, y, x_bolor, y_bolor):
    if(y < y_bolor):
        return x_bolor, y_bolor-1
    elif(y > y_bolor):
        return x_bolor, y_bolor+1
    elif(x > x_bolor):
        return x_bolor+1, y_bolor
    elif(x < x_bolor):
        return x_bolor-1, y_bolor

    return x_bolor, y_bolor #caso não possível no jogo normal



def trace_path(cell_details, dest, isKillingBvm = False):
    
    text = "BVM" if isKillingBvm else "Manteiga"

    print("Caminho: ", text, "\n")
    currentState = dest

    path = []
    i = 0

    while cell_details[currentState].pai != None:
        #input(f"Clique enter para continuar")
        print(i)
        print(currentState)
        path.append([currentState[0], currentState[1]])
        
        currentState = cell_details[currentState].pai
        print(currentState)
        i += 1

    path.append(currentState)
    path.reverse()

    for i in path:
        print("(", i[0], ", ", i[1], ")")
    return path


def a_star_search(tabuleiro, inicio, destino, bolor_position, isKillingBvm = False, posicoesManteiga = None):
    global numberStates

    manteigaCells = posicoesManteiga if posicoesManteiga is not None else [destino]

    if not is_valid(inicio[0], inicio[1], manteigaCells, bolor_position) or not is_valid(destino[0], destino[1], manteigaCells, bolor_position):
        print("Inicio ou destino inválido")
        return []

    # if not is_unblocked(tabuleiro, tabuleiro[inicio[0]][inicio[1]], inicio[0], inicio[1], inicio[0], inicio[1]):
    #     print("Inicio ou destino é bloqueado")
    #     return
    if isKillingBvm: 
        if is_destination(inicio[0], inicio[1], destino, isKillingBvm, bolor_position):
            print("Já bolor se queimou")
            return []
    else:
        if(is_destination(inicio[0], inicio[1], destino)):
            print("Já está no destino")
            return []

    closed_list_states = {}

    #cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]
    cell_details = {}

    x = inicio[0]
    y = inicio[1]
    bolor_x = bolor_position[0]
    bolor_y = bolor_position[1]

    state = (x, y, bolor_x, bolor_y)

    cell_details[state] = Cell()
    numberStates += 1

    cell_details[state].f = 0.0
    cell_details[state].g = 0.0
    cell_details[state].h = 0.0
    cell_details[state].pai = None


    open_list = []

    heapq.heappush(open_list, (0.0, x, y, bolor_x, bolor_y))

    found_dest = False

    while len(open_list) > 0:
        #print(len(open_list))
        p = heapq.heappop(open_list)

        x = p[1]
        y = p[2]

        x_bolor = p[3]
        y_bolor = p[4]

        state = (x, y, x_bolor, y_bolor)

        closed_list_states[state] = True

        #            abaixo,   acima, direita, esquerda
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            x_next = x + dir[0]
            y_next = y + dir[1]

            if(is_valid(x_next, y_next, manteigaCells, (x_bolor, y_bolor))):

                x_bolor_next, y_bolor_next = calculate_BVM_next_position(x_next, y_next, x_bolor, y_bolor)
                lastState = (x_next, y_next, x_bolor_next, y_bolor_next) #last state is a mistake (bolor variables must be the next ones)


                if is_valid(x_next, y_next, manteigaCells, (x_bolor_next, y_bolor_next)) and is_unblocked(tabuleiro, x, y, x_next, y_next, x_bolor, y_bolor) and lastState not in closed_list_states:
                    # if (isKillingBvm and is_destination(x_next, y_next, destino, isKillingBvm, (x_bolor, y_bolor))) or is_destination(x_next, y_next, destino):
                    if is_destination(x_next, y_next, destino, isKillingBvm, (x_bolor_next, y_bolor_next)):
                        
                        cell_details[lastState] = Cell()
                        numberStates += 1
                        cell_details[lastState].pai = state

                        print("Destino encontrado")
                        found_dest = True
                        return trace_path(cell_details, lastState, isKillingBvm)
                    else:
                        x_bolor_next = y_bolor_next = 0
                        g_next = cell_details[state].g + 1.0 #custo de movimento
                        h_next = 0

                        if isKillingBvm:
                            h_next, (x_bolor_next, y_bolor_next) = calculate_h_value_torradeira(x_next, y_next, x_bolor, y_bolor, posicoesManteiga, destino, tabuleiro[y_next][x_next])   
                        else:
                            h_next, (x_bolor_next, y_bolor_next) = calculate_h_value(x_next, y_next, x_bolor, y_bolor, destino, tabuleiro[y_next][x_next])
                        
                        f_next = g_next + h_next

                        nextState = (x_next, y_next, x_bolor_next, y_bolor_next)
                        cell_details[nextState] = Cell()
                        numberStates += 1

                        if cell_details[nextState].f == float('inf') or cell_details[nextState].f > f_next:
                            heapq.heappush(open_list, (f_next, x_next, y_next, x_bolor_next, y_bolor_next))

                            nextState = (x_next, y_next, x_bolor_next, y_bolor_next)

                            cell_details[nextState].f = f_next
                            cell_details[nextState].g = g_next
                            cell_details[nextState].h = h_next
                            cell_details[nextState].pai = state

    if not found_dest:
        print("Número de estados: ", numberStates)
        print("Destino não encontrado")

        return []


    



