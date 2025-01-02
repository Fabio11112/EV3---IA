import math
import heapq

COL = ROW = 6

class Cell:
    def __init__(self):
        self.pai = {
                    'x':0, 
                    'y':0
                    }

        # self.manteiga = 0
        # self.torradeira = 0
        # self.barreiras = {}


        #f = g + h
        self.f = float('inf')
        #cusuto total
        self.g = float('inf')
        #heuristica
        self.h = float('inf')

def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


"Uma célula é não bloqueada quando não tem barreiras na direção que se deseja ir OU não esteja o bolor na posição na que se quer ir"	
def is_unblocked(grid, x_before, y_before, x_next, y_next, x_bolor, y_bolor): 
    cell_before = grid[y_before][x_before]

    x_difference = x_before - x_next
    y_difference = y_before - y_next
    #print(f"({x_before}, {y_before}) -> ({x_next}, {y_next})")
    if(x_next == x_bolor and y_next == y_bolor):
        return False

    if(x_difference < 0 and cell_before.barreiras['Este']):
        return False
    elif(x_difference > 0 and cell_before.barreiras['Oeste']):
        return False
    elif(y_difference < 0 and cell_before.barreiras['Sul']):
        return False
    elif(y_difference > 0 and cell_before.barreiras['Norte']):
        return False

    return True

def is_destination(x, y, dest):
    return x == dest[0] and y == dest[1]


"Método que retorna a heurística da busca A* e também a seguinte posição do bolor de acordo com a posição atual"
def calculate_h_value(x, y, x_bolor, y_bolor, dest, celula):
    h_butter = abs(x - dest[0]) + abs(y - dest[1])
    butter_pos = dest
    penalty_bvm = 0
    penalty_bvm_butter = 0
    visited_penalty = 0

    bvm_next_x, bvm_next_y = calculate_BVM_next_position(x, y, x_bolor, y_bolor)



    print("HM")
    print(f"x: {x}, y: {y}")
    print("BVM before")
    print(f"x_bolor: {x_bolor}, y_bolor: {y_bolor}")
    print("BVM next")
    print(f"bvm_next_x: {bvm_next_x}, bvm_next_y: {bvm_next_y}")


    if(celula.visitada):
        visited_penalty = 10
    
    distance_to_bvm = abs(x - bvm_next_x) + abs(y - bvm_next_y)
    if distance_to_bvm == 0:
        penalty_bvm += 100  # Direct collision
    elif distance_to_bvm == 1:
        penalty_bvm += 20  # High risk
    # elif distance_to_bvm == 2:
    #     penalty_bvm += 20  # Moderate risk

    # Penalty for BVM being near Butter
    distance_bvm_butter = abs(bvm_next_x - butter_pos[0]) + abs(bvm_next_y - butter_pos[1])
    
    if distance_bvm_butter == 0:
        penalty_bvm_butter += 100  # BVM on Butter (critical)
    elif distance_bvm_butter == 1:
        penalty_bvm_butter += 50  # BVM adjacent to Butter

    print(f"h_butter: {h_butter}, \npenalty_bvm: {penalty_bvm}, \npenalty_bvm_butter: {penalty_bvm_butter}")

    return (h_butter + penalty_bvm + penalty_bvm_butter + visited_penalty, (bvm_next_x, bvm_next_y))


def calculate_BVM_next_position(x, y, x_bolor, y_bolor):
    if(y < y_bolor):
        return x_bolor, y_bolor-1
    elif(y > y_bolor):
        return x_bolor, y_bolor+1
    elif(x > x_bolor):
        return x_bolor+1, y_bolor
    elif(x < x_bolor):
        return x_bolor-1, y_bolor



def trace_path(cell_details, dest):
    print("\nCaminho: ")
    x= dest[0]
    y = dest[1]

    path = []

    while not (cell_details[x][y].pai['x'] == x and cell_details[x][y].pai['y'] == y):
        path.append([x, y])
        temp_x = cell_details[x][y].pai['x']
        temp_y = cell_details[x][y].pai['y']
        x = temp_x
        y = temp_y

    path.append([x, y])
    path.reverse()

    for i in path:
        print(f"({i[0]}, {i[1]})")
    print()


def a_star_search(tabuleiro, inicio, destino, bolor_position):
    if not is_valid(inicio[0], inicio[1]) or not is_valid(destino[0], destino[1]):
        print("Inicio ou destino inválido")
        return

    # if not is_unblocked(tabuleiro, tabuleiro[inicio[0]][inicio[1]], inicio[0], inicio[1], inicio[0], inicio[1]):
    #     print("Inicio ou destino é bloqueado")
    #     return
    if is_destination(inicio[0], inicio[1], destino):
        print("Já está no destino")
        return

    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]

    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    x = inicio[0]
    y = inicio[1]
    bolor_x = bolor_position[0]
    bolor_y = bolor_position[1]

    cell_details[x][y].f = 0.0
    cell_details[x][y].g = 0.0
    cell_details[x][y].h = 0.0
    cell_details[x][y].pai['x'] = x
    cell_details[x][y].pai['y'] = y


    open_list = []

    heapq.heappush(open_list, (0.0, x, y, bolor_x, bolor_y))

    found_dest = False

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        x = p[1]
        y = p[2]

        x_bolor = p[3]
        y_bolor = p[4]

        closed_list[x][y] = True

        #            abaixo,   acima, direita, esquerda
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            x_next = x + dir[0]
            y_next = y + dir[1]

            if is_valid(x_next, y_next) and is_unblocked(tabuleiro, x, y, x_next, y_next, x_bolor, y_bolor) and not closed_list[x_next][y_next]:
                if is_destination(x_next, y_next, destino):
                    cell_details[x_next][y_next].pai['x'] = x
                    cell_details[x_next][y_next].pai['y'] = y
                    print("Destino encontrado")
                    trace_path(cell_details, destino)
                    found_dest = True
                    return
                else:
                    x_bolor_next = y_bolor_next = 0
                    g_next = cell_details[x][y].g + 1.0
                    h_next, (x_bolor_next, y_bolor_next) = calculate_h_value(x_next, y_next, x_bolor, y_bolor, destino, tabuleiro[y_next][x_next])
                    f_next = g_next + h_next

                    if cell_details[x_next][y_next].f == float('inf') or cell_details[x_next][y_next].f > f_next:
                        heapq.heappush(open_list, (f_next, x_next, y_next, x_bolor_next, y_bolor_next))

                        cell_details[x_next][y_next].f = f_next
                        cell_details[x_next][y_next].g = g_next
                        cell_details[x_next][y_next].h = h_next
                        cell_details[x_next][y_next].pai['x'] = x
                        cell_details[x_next][y_next].pai['y'] = y

    if not found_dest:
        print("Destino não encontrado")


    



