import queue
import math
from scipy.spatial.distance import cityblock

'''Advanced form of BFS algorithm

    f(n) -> cost path from start to goal = h + g.
    h(n) -> cost path from actual node to goal.
    g(n) -> cost path from start to actual node.


    TODO:
    algorithm
    'h' will be the manhattan distance
    nodes and their edges, weights
    add obstacles in certain positions, make those positions invalid for the search
'''


class Cell:
    def __init__(self, h, g, pos, id):
        self.h = h
        self.g = g
        self.f = h + g
        self.pos = pos
        self.id = id
        self.tag = "cell"
        self.possibleDir = []


class Obstacle:
    def __init__(self, pos):
        self.pos = pos
        self.tag = "Obstacle"


# cambiar esto
adj_list = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 12)]
}

pos_inf = float('inf')
rows, cols = (4, 4)
matrix = []
directions = {
    'left': [(0, 1)],
    'right': [(0, -1)],
    'up': [(1, 0)],
    'down': [(-1, 0)]
}
counter = 0

# preparation of the grid/matrix and its cells.
for i in range(rows):
    col = []
    for j in range(cols):
        if (i + 1 == rows and j + 1 == cols):
            col.append(Cell(pos_inf, 0, (i+1, j+1), counter))
        else:
            col.append(Cell(pos_inf, pos_inf, (i+1, j+1), counter))
        counter += 1
        # print(col[j].id)
    matrix.append(col)


# arr = [[positive_infinity] * cols] * rows
# neighbors - Mis neighbors son las celdas adyacentes, derecha, izquierda, arriba y abajo, tener algo para filtrar out of range

'''
izq -1 en x
der +1 en x
arriba +1 y
abajo -1 en y

la frontera está cuando se pasa rows y cols con 5
o cuando se baja a 0.
'''

''' Recives two cells or nodes and it calcules the distance.
    It is the h(n) or heuristic function. '''


def manhattanDistance(pointA, pointB):

    # combined = zip(pointB, pointA)
    distance = 0

    # both input points should have equal length
    for i in range(len(pointA)):
        distance += (pointB[i - 1] - pointA[i])

    print(distance)
    return distance

# receives the matrix, goal and start.


def a_start_search(goal, start, matrix, directions):

    open = []
    close = []
    currentCell = None

    open.append(start)
    while (not open.empty() or open[0] == goal):
        # despues del pop se recorre la lista, entonces puedo meter a todos las celdas, pero solo voy a meter a los vecinos
        currentCell = open.pop(0)
        for d in directions:
            # current cell se mueve a todas las 4 posibles posiciones, las que son validas se guardan en possibleDir de la propia cell. Elige una aleatoria, se hace el algoritmo
            print("pending")


# positions as tuples
A = (2, 4)
B = (5, 5)

manhattanDistance(A, B)
print(cityblock(A, B))
