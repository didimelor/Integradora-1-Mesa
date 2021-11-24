import math
import sys
from mesa import Agent


def getDistance(A, B):
    distance = 0
    if (B[0] != A[0] and B[1] != A[1]):
        distance = math.sqrt(math.pow((B[0] - A[0]), 2)
                             + math.pow((B[1] - A[1]), 2))
    return distance


def closerPoints(possible_steps, base):

    n = len(possible_steps)
    distance = sys.float_info.max
    closest = -1
    currDistance = 0

    # O(n)
    for i in range(n):
        currDistance = getDistance(possible_steps[i], base)
        # For the very first iteration this is always true.
        if (currDistance < distance):
            closest = possible_steps[i]
            distance = currDistance

    return closest


class Robot(Agent):

    def __init__(self, unique_id, model, base):
        super().__init__(unique_id, model)
        self.direction = 4  # 1UP 3LEFT 4CENTER 5RIGHT 7DOWN
        self.hasBox = False
        self.box = None
        self.target = base
        self.allDirections = [1, 3, 4, 5, 7]

    def move(self):
        # important: get_neighbor for objects, get_neighborhood for positions.
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True)

        # print(f"PRINT = {possible_steps}")
        self.direction = self.random.choice(possible_steps)
        # print(f"PRINT = {possible_steps}")
        # print(f"SECOND = {self.direction}")
        # print(f"THIRD = {self.direction}")

        # self.pos = self.direction : esta linea hace que haya crash

        # crear lista con las direcciones valides despues de hacer un scan como linea 53 y luego moverme
        # for i in self.model.grid.get_cell_list_contents(self.pos):
        # if (isinstance(b, Box) or isinstance(a, Robot)):
        # possible_directions =

        # pick-up a box if not already holding one.
        for b in self.model.grid.get_cell_list_contents(self.pos):
            if (isinstance(b, Box) and b.condition == "unstoraged"
                    and not self.hasBox):
                self.hasBox = True
                b.condition = "picked-up"
                self.box = b
                b.move(self.pos)

        self.model.grid.move_agent(self, self.direction)
        # b.model.grid.move_agent(self, possible_steps[self.direction])

    def move2Base(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True)

        # choose the best possible step.
        self.direction = closerPoints(possible_steps, self.target)
        # move the robot closer to the base.
        self.model.grid.move_agent(self, self.direction)
        # move the box along the robot.
        self.box.move(self.direction)

    def step(self):
        # self.move()
        if (self.pos == self.target):
            self.box.condition = "storaged"
            self.hasBox = False
            print("Returned to base, box delivered!")
            self.move()
            print("Going back to explore!")

        elif (self.hasBox and self.pos != self.target):
            self.move2Base()

        else:
            self.move()


class Box(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)  # id
        self.id = id
        self.pos = pos
        self.condition = "unstoraged"

    # move box when I'm picked up by a robot.
    def move(self, robot_pos):
        self.pos = robot_pos

    def step(self):
        pass
        # if self.condition == "picked-up":
        # self.move()


"""
TODO:
lista de obstáculos, [lista para cada obstaculo, que guarde sus 3 posiciones más recientes]
comunicación entre robots para que uno se quede parado mientras el otro avanza o si ambos traen caja OR ambos no tiene caja echen volado para ver quien va
lo de la función inform a mis vecinos traigo caja ahi te voy
"""
