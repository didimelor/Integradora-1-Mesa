from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import Box, Robot


class FloorTiles(Model):

    def __init__(self, height=100, width=100, density=0.65, numberRobots=1,
                 counter=0, max=100, base=(0, 100)):

        # Set up model objects
        self.num_robots = numberRobots
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)
        self.counter = counter
        self.max = max

        self.datacollector = DataCollector(
            {
                "unstoraged": lambda m: self.count_type(m, "unstoraged"),
                "storaged": lambda m: self.count_type(m, "storaged"),
                "picked-up": lambda m: self.count_type(m, "picked-up")
            }
        )

        # create and place agents
        for i in range(self.num_robots):
            # agent = Rumba(i, (1, 1), self)
            agent = Robot(i, self, base)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        # Place a Box according to probability
        _id = 0
        for (contents, x, y) in self.grid.coord_iter():
            new_box = Box((x, y), self)

            # edtar linea 41
            if self.random.random() < density:
                new_box.condition = "unstoraged"
                new_box.id = _id
                _id += 1

            self.grid.place_agent(new_box, (x, y))
            self.schedule.add(new_box)

        # for nV in range(0, numberRobots):
            # a = Robot(nV+1000, self, base)
            # self.schedule.add(a)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # robot(s) finished collecting boxes.
        if self.count_type(self, "unstoraged") == 0:
            self.running = False

        # if the tolerance is reached, finish the simulation.
        if self.counter == self.max:
            print(f"The max was reached: {self.counter}")
            self.running = False
        else:
            self.counter += 1

    @staticmethod
    def count_type(model, cond):
        count = 0
        for ft in model.schedule.agents:
            if(isinstance(ft, Box)):
                if ft.condition == cond:
                    count += 1
        return count
