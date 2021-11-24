from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from model import FloorTiles 
from agent import caja, cargador

COLORS = ["#FFC0CB", "#A8C0D3"]  #pink es el cargador


def floor_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}

    if(isinstance(agent, cargador)):
    	(x, y) = agent.pos
    	portrayal["x"] = x
    	portrayal["y"] = y
    	portrayal["Color"] = COLORS[0]

    elif(isinstance(agent, caja)):
        portrayal["Color"] = COLORS[1]
        portrayal["Layer"] = 1
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1        

    return portrayal

canvas_element = CanvasGrid(floor_portrayal, 10, 10, 500, 500)

model_params = {
	"height": UserSettableParameter("slider", "Height", 10, 100, 500, 1),
	"width": UserSettableParameter("slider", "Width", 10, 100, 500, 1),
    "density": UserSettableParameter("slider", "Densidad de cajas", 0.65, 0.01, 1.0, 0.01),
    "numberCargadores": UserSettableParameter("slider", "Cargadores num", 3, 1, 10, 1),
    "basex": 0,
    "basey": 4,
}

server = ModularServer(FloorTiles, [canvas_element], "Almacen", model_params)

server.launch()