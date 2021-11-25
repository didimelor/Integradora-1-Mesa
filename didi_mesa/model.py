from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import random

from agent import caja, cargador

class FloorTiles(Model):

    def __init__(self, height=100, width=100, density=0.65, numberCargadores=1, basex = 0, basey = 0):

        super().__init__()
        self.num_carg = numberCargadores
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(height, width, torus=False)
        self.basex = basex
        self.basey = basey

        for i in range(numberCargadores):
            xpos = random.randrange(0, width)
            ypos = random.randrange(0, height)
            char = cargador(i+1000, (xpos, ypos), (basex,basey), self)
            self.schedule.add(char)
            self.grid.place_agent(char, (xpos, ypos))

        for (contents, x, y) in self.grid.coord_iter():
            agent = caja((x, y), (basex, basey), self)
            if self.random.random() < density:
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
        self.running = True

    def step(self):
        self.schedule.step()
        if self.count_type() == 0:
            self.running = False

    def count_type(self):
        count = 0
        for ft in self.schedule.agents:
            if(isinstance(ft, caja) and ft.pos != (self.basex, self.basey)):
                count += 1
        return count





