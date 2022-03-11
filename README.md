# Prey - Predator Model

At each time step, only one action is performed by the sheep or wolves (i.e. reproduce or eat). The sheep eat grass and wolves eat sheep. We consider that sheep eat all grass available when they moved on a cell. The grass grows with a certain speed and sheep can eat it before it is fully grown (however, they get less energy by doing so). Both wolves and sheep make "smart" moves, i.e. a sheep won't go on a cell where there is a wolf and will move to the cell where is the more food. The decision of sheep or wolves to eat or to reproduce is done according to the hormones and hunger variables. Also, a wolf won't eat a sheep if he has an energy level higher than a certain threshold as a  wolf does not have an infinitely expandable stomach. We considered that this rule isn't essential in the case of sheep.

We defined genders for sheep and wolves. Thus, we defined ram and ewe and wolves and she-wolves. Reproduction occurs only with a certain probability when a female and male gender meet. Only one cub is obtained after reproduction. To increase realism, we added an age parameter. The born cub has an age of 0. At each time step, the age is increased by one. The age parameters is also used to fix age limits and illness probability. The older becomes the sheep, the higher is the probability that he dies with a limit of 100 steps. After a certain threshold, agents will die from old age.




## Summary

A simple ecological model, consisting of three agent types: wolves, sheep, and grass. The wolves and the sheep wander around the grid at random. Wolves and sheep both expend energy moving around, and replenish it by eating. Sheep eat grass, and wolves eat sheep if they end up on the same grid cell.

If wolves and sheep have enough energy, they reproduce, creating a new wolf or sheep (in this simplified model, only one parent is needed for reproduction). The grass on each cell regrows at a constant rate. If any wolves and sheep run out of energy, they die.

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (wolves, sheep, grass)
 - Overlay arbitrary text (wolf's energy) on agent's shapes while drawing on CanvasGrid
 - Agents inheriting a behavior (random movement) from an abstract parent
 - Writing a model composed of multiple files.
 - Dynamically adding and removing agents from the schedule

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``prey_predator/random_walker.py``: This defines the ``RandomWalker`` agent, which implements the behavior of moving randomly across a grid, one cell at a time. Both the Wolf and Sheep agents will inherit from it.
* ``prey_predator/agents.py``: Defines the Wolf, Sheep, and GrassPatch agent classes.
* ``prey_predator/schedule.py``: Defines a custom variant on the RandomActivation scheduler, where all agents of one class are activated (in random order) before the next class goes -- e.g. all the wolves go, then all the sheep, then all the grass.
* ``prey_predator/model.py``: Defines the Prey-Predator model itself
* ``prey_predator/server.py``: Sets up the interactive visualization server
* ``run.py``: Launches a model visualization server.

## Results

![screen-gif](images/Animation3.gif)

## Further Reading

This model is closely based on the NetLogo Wolf-Sheep Predation Model:

Wilensky, U. (1997). NetLogo Wolf Sheep Predation model. http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

See also the [Lotka–Volterra equations
](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) for an example of a classic differential-equation model with similar dynamics.
