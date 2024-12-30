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

def is_unblocked(grid, x_before, y_before, x_next, y_next):
    cell_before = grid[x_before][y_before]

    x_difference = x_before - x_next
    y_difference = y_before - y_next

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

def calculate_h_value(x, y, dest):
    return abs(x - dest[0]) + abs(y - dest[1])

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


def a_star_search(tabuleiro, inicio, destino):
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
    cell_details[x][y].f = 0.0
    cell_details[x][y].g = 0.0
    cell_details[x][y].h = 0.0
    cell_details[x][y].pai['x'] = x
    cell_details[x][y].pai['y'] = y


    open_list = []
    heapq.heappush(open_list, (0.0, x, y))

    found_dest = False

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        x = p[1]
        y = p[2]

        closed_list[x][y] = True

        #            abaixo,   acima, direita, esquerda
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            x_next = x + dir[0]
            y_next = y + dir[1]

            if is_valid(x_next, y_next) and is_unblocked(tabuleiro, x, y, x_next, y_next) and not closed_list[x_next][y_next]:
                if is_destination(x_next, y_next, destino):
                    cell_details[x_next][y_next].pai['x'] = x
                    cell_details[x_next][y_next].pai['y'] = y
                    print("Destino encontrado")
                    trace_path(cell_details, destino)
                    found_dest = True
                    return
                else:
                    g_next = cell_details[x][y].g + 1.0
                    h_next = calculate_h_value(x_next, y_next, destino)
                    f_next = g_next + h_next

                    if cell_details[x_next][y_next].f == float('inf') or cell_details[x_next][y_next].f > f_next:
                        heapq.heappush(open_list, (f_next, x_next, y_next))

                        cell_details[x_next][y_next].f = f_next
                        cell_details[x_next][y_next].g = g_next
                        cell_details[x_next][y_next].h = h_next
                        cell_details[x_next][y_next].pai['x'] = x
                        cell_details[x_next][y_next].pai['y'] = y

    if not found_dest:
        print("Destino não encontrado")


    



