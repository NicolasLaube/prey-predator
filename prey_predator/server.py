from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    if type(agent) is Sheep:
        return {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
    if type(agent) is Wolf:
        return {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if type(agent) is GrassPatch:
        return {
            "Shape": "rectangle",
            "Filled": "true",
            "Color": "green"
        }


# portrayal = {"Shape": "circle",
#                  "Filled": "true",
#                  "r": 0.5}

#     if agent.wealth > 0:
#         portrayal["Color"] = "red"
#         portrayal["Layer"] = 0
#     else:
#         portrayal["Color"] = "grey"
#         portrayal["Layer"] = 1
#         portrayal["r"] = 0.2
#     return portrayal

# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')
# grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
# server = ModularServer(MoneyModel,
#                    [grid, chart],
#                    "Money Model",
#                    {"width":10, "height":10, "density": UserSettableParameter("slider", "Agent density", 0.8, 0.1, 1.0, 0.1)})
# server.port = 8521 # The default
# server.launch()



canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    # ... to be completed
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
