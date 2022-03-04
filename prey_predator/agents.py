from typing import Tuple
from mesa import Agent, Model
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.moore = moore
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if cellmate.pos == self.pos:
                self.model.schedule.
        
        # ... to be completed


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, reproduction_probability, gain_from_food, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.reproduction_probability = reproduction_probability
        self.gain_from_food = gain_from_food
        self.unique_id = unique_id
        self.model = model
        self.pos = pos
        self.moore = moore
        self.current_energy = self.energy

    def step(self):
        self.random_move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if type(cellmate) is Sheep :
                self.enery += self.gain_from_food
                self.model.schedule.remove(cellmate)
                break
        if self.random.random() <= self.reproduction_probability:
            wolf_cub = Wolf(self.model.schedule.get_breed_count(Wolf), self.pos, self.model, self.moore, self.reproduction_probability, self.gain_from_food, self.energy)
            self.model.schedule.add()
        self.current_energy -= 1
        if self.current_energy == 0:
            self.model.schedule.remove(self)



class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id: int, pos: Tuple[int, int], model: Model, fully_grown: bool, countdown: int):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.time_before_fully_grown = countdown

    def step(self):
        if not self.fully_grown:
            if self.time_before_fully_grown == 0:
                self.time_before_fully_grown = self.countdown
            self.time_before_fully_grown -= 1
            if self.time_before_fully_grown == 0:
                self.fully_grown = True
