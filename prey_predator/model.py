"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed
from prey_predator.utils import Sex


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    # height = 20
    # width = 20

    # initial_sheep = 100
    # initial_wolves = 50

    # sheep_reproduce = 0.04
    # wolf_reproduce = 0.05

    # wolf_gain_from_food = 20

    # grass = False
    # grass_regrowth_time = 30
    # sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        moore=True,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        sheep_gain_from_food=4,
        wolf_gain_from_food=20,
        sheep_initial_energy=6,
        wolves_initial_energy=6,
        grass_regrowth_time=30,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            sheep_gain_from_food: Energy sheep gain from grass, if enabled
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            sheep_initial_energy: Initial energy of the sheep
            worlves_initial_energy: Initial energy of the wolves
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.sheep_gain_from_food = sheep_gain_from_food
        self.wolf_gain_from_food = wolf_gain_from_food
        self.sheep_initial_energy = sheep_initial_energy
        self.wolves_initial_energy = wolves_initial_energy
        self.grass_regrowth_time = grass_regrowth_time

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        self.current_nb_agents = 0
        # Create sheep:
        for _ in range(initial_sheep):
            x, y = self.grid.find_empty()
            size = random.random() * 0.5 + 0.5
            sex = Sex.Male if bool(random.getrandbits(1)) else Sex.Female

            sheep = Sheep(
                self.current_nb_agents,
                (x, y),
                self,
                moore,
                sheep_reproduce,
                sheep_gain_from_food,
                sheep_initial_energy,
                size,
                sex,
            )
            self.schedule.add(sheep)
            self.grid.place_agent(sheep, (x, y))
            self.current_nb_agents += 1

        # Create wolves
        for _ in range(initial_wolves):
            x, y = self.grid.find_empty()
            size = random.random() * 0.5 + 0.5
            sex = Sex.Male if bool(random.getrandbits(1)) else Sex.Female
            wolf = Wolf(
                self.current_nb_agents,
                (x, y),
                self,
                moore,
                wolf_reproduce,
                wolf_gain_from_food,
                6,
                size,
                sex,
            )
            self.schedule.add(wolf)
            self.grid.place_agent(wolf, (x, y))
            self.current_nb_agents += 1

        # Create grass patches
        for x in range(self.width):
            for y in range(self.height):
                grass = GrassPatch(
                    self.current_nb_agents, (x, y), self, True, grass_regrowth_time
                )
                self.schedule.add(grass)
                self.grid.place_agent(grass, (x, y))
                self.current_nb_agents += 1

        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )
        self.datacollector.collect(self)

    def step(self):
        # Collect data
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()
