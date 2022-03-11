# Modèle proie prédateur

At each time step, only one action is performed by the sheep or wolves (i.e. reproduce or eat). The sheep eat grass and wolves eat sheep. We consider that sheep eat all grass available when they moved on a cell. The grass grows with a certain speed and sheep can eat it before it is fully grown (however, they get less energy by doing so). Both wolves and sheep make "smart" moves, i.e. a sheep won't go on a cell where there is a wolf and will move to the cell where is the more food. The decision of sheep or wolves to eat or to reproduce is done according to the hormones and hunger variables. After reproduction, hormones are low to prevent multiple reproductions and favour energy intake. The same is true for the hunger variable. Also, a wolf won't eat a sheep if he has an energy level higher than a certain threshold as a  wolf does not have an infinitely expandable stomach. We considered that this rule isn't essential in the case of sheep.

We defined genders for sheep and wolves. Thus, we defined ram and ewe and wolves and she-wolves. Reproduction occurs only with a certain probability when a female and male gender meet. Only one cub is obtained after reproduction. To increase realism, we added an age parameter. The born cub has an age of 0. At each time step, the age is increased by one. The age parameters is also used to fix age limits and illness probability. The older becomes the sheep, the higher is the probability that he dies with a limit of 100 steps. After a certain threshold, agents will die from old age. Finally, the age is used to set a minimal reproduction age (this assumption also prevents that a cub immediately reproduces with one of his parents).




## Summary
## Résumé

![screen-gif](images/Animation3.gif)

Nous avons conçu un modèle multi-agent pour simuler un système de proies (représentées par des moutons) et prédateurs (représentés par des loups).

L'objectif de ce modèle est d'observer des mécanismes de régulation pouvant se mettre en place, notamment

- Si le système peut s'équilibrer, le nombre de proies ou de prédateurs ne chutant jamais à 0
- Si les proies meurent en l'absence de prédateurs (en épuisant toutes les ressources)

## Paramètres de la simulation

Nous avons modifié sensiblement les agents:

- Les moutons et les loups ont maintenant un **sexe**, et ils doivent trouver un partenaire du sexe opposé pour s'accoupler.
- Les moutons et les loups ont un **âge** : ils prennent un certain temps à atteindre l'âge adulte, et plus ils sont vieux et plus ils ont de chance de mourir de maladie ou de vieillesse.
- Les loups et les moutons **se dirigent intelligemment** en regardant le contenu des cases à côté d'eux à tout instant.
- Les loups ont une notion de **faim** ; les loups et les moutons ont une notion d'**hormones**. Celles-ci influent leur comportement, pour que par exemple un animal ne s'étant pas accouplé depuis longtemps cherche avant tout un partenaire (par rapport à la nourriture), et inversement.
- Les moutons peuvent **manger l'herbe même si elle n'a pas entièrement poussé**. Dans ce cas, ils ne récupèreront qu'une partie de l'énergie d'une herbe qui a fini de pousser.

## Implémentation

La structure de fichiers n'a pas changé.

Les différentes actions possibles des agents ont par contre été séparées dans différentes méthodes, notamment pour les moutons et les loups:

- La méthode _step_ est la méthode principale d'update. Elle appelle les actions possibles.
- La méthode _choose_move_ permet aux individus de choisir la case pour le prochain déplacement.
- La méthode _reproduce_, couplée avec la méthode _can_reproduce_with_, leur permettent de se reproduire.
- La méthode _update_energy_ leur permet de manger.

## Affichage

## Results

![screen-gif](images/Animation3.gif)

## Further Reading
Nous avons choisi de représenter les différents agents à l'aide des images suivantes:

- Les loups\
   ![Wolf male](./images/agents/wolf.png)
- Les louves\
   ![Wolf female](./images/agents/shewolf.png)
- Les béliers\
   ![Sheep male](./images/agents/belier.png)
- Les brebis\
   ![Sheep female](./images/agents/sheep.png)
- L'herbe (haute à gauche, broutée à droite)\
   ![Grass](./images/agents/grass.png)

Les petits des loups et des moutons sont juste représentés de taille moins grande que les adultes.\
![Cubs](./images/agents/cubs.png)

Sur l'affichage, nous pouvons voir les éléments suivants:

- La **barre supérieure** présentant le modèle et permettant de le démarrer, de le stopper et de le mettre à zéro
- La **grille** avec les agents
- Les **paramètres du modèles**, que l'on peut modifier
- Un **graph** présentant la répartition des loups et des moutons au cours du temps

![Screen](./images/full_screen.png)

#

## Résultats
