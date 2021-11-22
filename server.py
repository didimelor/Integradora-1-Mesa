from model import FloorTiles
from agent import Robot, Box
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule


COLORS = {"unstoraged": "#900C3F",
          "storaged": "#12EFB9",
          "picked-up": "#F324A5"}


def floor_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}

    if(isinstance(agent, Box)):
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = COLORS[agent.condition]

    elif(isinstance(agent, Robot)):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal


canvas_element = CanvasGrid(floor_portrayal, 10, 10, 500, 500)

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": UserSettableParameter("slider", "Height", 10, 100, 500, 1),
    "width": UserSettableParameter("slider", "Width", 10, 100, 500, 1),
    "density": UserSettableParameter("slider", "Unstoraged quantity",
                                     0.65, 0.01, 1.0, 0.01),
    "numberRobots": UserSettableParameter("slider", "Robot quantity",
                                          1, 1, 10, 1),
    "max": UserSettableParameter("slider", "Max", 10, 10, 150, 1),
}

server = ModularServer(FloorTiles, [canvas_element, tree_chart,
                       pie_chart], "Robots searching", model_params)

server.launch()
