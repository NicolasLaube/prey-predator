from typing import Tuple
import random
from mesa import Agent, Model
from prey_predator.random_walk import RandomWalker
from prey_predator.utils import Sex
from prey_predator import config


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(
        self,
        unique_id,
        pos,
        model,
        moore,
        reproduction_probability,
        gain_from_food,
        energy,
        age,
        sex,
    ):
        super().__init__(unique_id, pos, model, moore=moore)
        self.reproduction_probability = reproduction_probability
        self.gain_from_food = gain_from_food
        self.energy = energy
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.moore = moore

        self.age = age
        self.sex = sex
        self.hormones: float = 0

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        is_dead = self.die_from_age_or_illness()

        if not is_dead:

            if self.has_grown_up_sheep(cellmates):
                if self.random.random() <= self.reproduction_probability:
                    self.reproduce()
                    self.random_move()
                else:
                    self.choose_move()
            else:
                self.choose_move()
            self.update_energy()
            self.hormones += 0.1

    def has_grown_up_sheep(self, cellmates) -> bool:
        """Says if cell contains other sheep"""
        for cellmate in cellmates:
            if (
                type(cellmate) is Sheep
                and cellmate.unique_id != self.unique_id
                and cellmate.age >= config.SHEEP_ADULT_AGE
                and cellmate.sex != self.sex
            ):
                return True
        return False

    def die_from_age_or_illness(self):
        """Dies from age or illness"""
        if self.age > config.SHEEP_MAX_AGE:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return True
        if (
            self.age > config.SHEEP_CAN_BECOME_ILL_FROM
            and random.randint(0, config.SHEEP_MAX_AGE - self.age) == 0
        ):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return True
        return False

    def choose_move(self):
        """Choose a move"""
        neighboring_cells = self.model.grid.get_neighborhood(
            self.pos, self.moore, include_center=True
        )

        candidate_cells = []

        for cell_pos in neighboring_cells:
            cell_agents = self.model.grid.get_cell_list_contents(cell_pos)
            add_cell = True
            cell_score = 0

            for agent in cell_agents:
                if type(agent) is Wolf:
                    add_cell = False

                if self.can_reproduce_with(agent):
                    cell_score += self.hormones

                elif (
                    type(agent) is GrassPatch
                    and self.energy < config.SHEEP_HUNGER_ENERGY
                ):
                    cell_score += agent.fully_grown

            if add_cell:
                candidate_cells.append((cell_pos, cell_score))
        random.shuffle(candidate_cells)
        candidate_cells = sorted(candidate_cells, key=lambda x: x[1])

        self.model.grid.move_agent(self, candidate_cells[-1][0])

    def is_adult(self):
        """Is the sheep adult?"""
        return self.age >= 5

    def can_reproduce_with(self, agent):
        """Can the sheep reproduce with the other agent?"""
        if type(agent) != type(self):
            return False
        if self.sex == agent.sex:
            return False
        if not self.is_adult() or not agent.is_adult():
            return False
        if self.unique_id == agent.unique_id:
            return False

        return True

    def reproduce(self):
        """Sheep reproduction"""
        self.model.current_nb_agents += 1
        sex = Sex.Male if bool(random.getrandbits(1)) else Sex.Female

        sheep_cub = Sheep(
            self.model.current_nb_agents,
            self.pos,
            self.model,
            self.moore,
            self.reproduction_probability,
            self.gain_from_food,
            energy=config.SHEEP_INITIAL_ENERGY,
            age=0,
            sex=sex,
        )
        self.model.schedule.add(sheep_cub)
        self.model.grid.place_agent(sheep_cub, self.pos)
        self.energy -= 1
        self.hormones = 0
        print(f"Sheep cub born, id={self.model.current_nb_agents}")

    def update_energy(self):
        """Sheep energy update"""
        self.age += 1

        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        for cellmate in cellmates:
            if type(cellmate) is GrassPatch and cellmate.fully_grown:
                self.energy += self.gain_from_food * cellmate.fully_grown
                cellmate.is_eaten()
                break
        self.energy -= 1

        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(
        self,
        unique_id,
        pos,
        model,
        moore,
        reproduction_probability,
        gain_from_food,
        energy,
        age,
        sex,
    ):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.reproduction_probability = reproduction_probability
        self.gain_from_food = gain_from_food
        self.unique_id = unique_id
        self.model = model
        self.pos = pos
        self.moore = moore
        self.age = age

        self.hunger = 1
        self.hormones = 1
        self.sex = sex

    def step(self):
        self.choose_move()

        if not self.die_from_age_or_illness():

            cellmates = self.model.grid.get_cell_list_contents([self.pos])

            if self.has_other_grown_up_wolf(cellmates):
                # reproduce with certain probability or move
                if self.random.random() <= self.reproduction_probability:
                    self.reproduce()
                    self.random_move()
                else:
                    self.choose_move()
                    self.hormones += 0.1
            else:
                self.choose_move()
                self.hormones += 0.1

            self.update_energy(cellmates)

    def die_from_age_or_illness(self):
        """Dies from age or illness"""
        if self.age > config.WOLF_MAX_AGE:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return True
        if (
            self.age > config.WOLF_CAN_BECOME_ILL_FROM
            and random.randint(0, config.WOLF_MAX_AGE - self.age) == 0
        ):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return True
        return False

    def has_other_grown_up_wolf(self, cellmates) -> bool:
        """Says if cell contains other wolves"""
        for cellmate in cellmates:
            if (
                type(cellmate) is Wolf
                and cellmate.unique_id != self.unique_id
                and cellmate.age >= config.WOLF_ADULT_AGE
                and self.sex != cellmate.sex
            ):
                return True
        return False

    def update_energy(self, cellmates):
        """Update energy"""
        self.age += 1

        ate_something = False
        for cellmate in cellmates:
            if type(cellmate) is Sheep:
                print(
                    f"A sheep was eaten id={cellmate.unique_id} in pos={cellmate.pos}"
                )
                self.energy += self.gain_from_food
                self.model.grid.remove_agent(cellmate)
                self.model.schedule.remove(cellmate)
                ate_something = True
                break

        if ate_something:
            self.hunger = 0
        else:
            self.hunger += 1

        self.energy -= 1
        if self.energy <= 0:
            print(f"A wolf died id={self.unique_id} in pos={self.pos}")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def choose_move(self):
        """Choose move"""
        neighboring_cells = self.model.grid.get_neighborhood(
            self.pos, self.moore, include_center=True
        )

        candidate_cells = []

        for cell_pos in neighboring_cells:
            cell_agents = self.model.grid.get_cell_list_contents(cell_pos)
            cell_score = 0

            for agent in cell_agents:
                if (
                    type(agent) is Wolf
                    and agent.unique_id != self.unique_id
                    and agent.age >= config.WOLF_ADULT_AGE
                    and self.sex != agent.sex
                ):
                    cell_score += self.hormones
                if type(agent) is Sheep and self.energy < 10:
                    cell_score += self.hunger * agent.age
            candidate_cells.append((cell_pos, cell_score))

        random.shuffle(candidate_cells)
        candidate_cells = sorted(candidate_cells, key=lambda x: x[1])

        self.model.grid.move_agent(self, candidate_cells[-1][0])

    def reproduce(self):
        """Reproduction of Wolf"""
        self.model.current_nb_agents += 1
        sex = Sex.Male if bool(random.getrandbits(1)) else Sex.Female

        wolf_cub = Wolf(
            self.model.current_nb_agents,
            self.pos,
            self.model,
            self.moore,
            self.reproduction_probability,
            self.gain_from_food,
            energy=config.WOLF_INITIAL_ENERGY,
            age=0,
            sex=sex,
        )
        self.model.schedule.add(wolf_cub)
        self.model.grid.place_agent(wolf_cub, self.pos)
        self.hormones = 0
        self.energy -= 1
        print(f"Wolf cub born, id={self.model.current_nb_agents}")


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(
        self,
        unique_id: int,
        pos: Tuple[int, int],
        model: Model,
        fully_grown: float,
        countdown: int,
    ):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
            fully_grown: between 0 and 1 (represents age of grass)
        """
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        """One setp for grass"""
        self.fully_grown = min(self.fully_grown + 1 / self.countdown, 1)

    def is_eaten(self):
        self.fully_grown = 0
