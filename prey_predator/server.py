from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def combine_hex_values(color1, color2, proportion):
    red = int(
        proportion * int(color1[1:3], 16) + (1 - proportion) * int(color2[1:3], 16)
    )
    green = int(
        proportion * int(color1[3:5], 16) + (1 - proportion) * int(color2[3:5], 16)
    )
    blue = int(
        proportion * int(color1[5:7], 16) + (1 - proportion) * int(color2[5:7], 16)
    )
    zpad = lambda x: x if len(x) == 2 else "0" + x
    return f"#{zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])}"


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    if type(agent) is Sheep:
        return {
            "Shape": "./prey_predator/images/sheep.png",
            "Layer": 1,
        }
    if type(agent) is Wolf:
        return {
            "Shape": "./prey_predator/images/wolf.png",
            "Layer": 2,
        }

    if type(agent) is GrassPatch:
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "green",
            "w": 1,
            "h": 1,
        }
        portrayal["Color"] = combine_hex_values(
            "#2da501", "#f2ff74", 1 - agent.time_before_fully_grown / agent.countdown
        )
        return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    "height": 20,
    "width": 20,
    "moore": True,
    "initial_sheep": 100,
    "initial_wolves": 50,
    "sheep_reproduce": 0.5,
    "wolf_reproduce": 0.05,
    "wolf_gain_from_food": 20,
    "grass": False,
    "grass_regrowth_time": 30,
    "sheep_gain_from_food": 4,
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
