# Genetic-Algorithm-Burger-King
A Python 3.7.1 framework and Evolution-based manager script.  
Aim: 
1. To set up an environment to experiment with Genetic Evolution Algorithms. 
2. To make it modular so anyone can use it and improve on it.

## The Game itself
### The environment and premise
Put a "gene-controlled robot" on a square grid playing field of a specific size. Some locations of the playing field have food, and the rest are empty. The field is surrounded by walls, so the robot cannot fall out of the field. The simulator/framework/API accepts these parameters:
1. ***seed***: Int. The seed to be fed into the random number generator. This decides where the food and robot are placed on the map. Defaults to "711".
2. ***size***: Int. The size of the *usable* grid, excluding walls. The grid is square. Defaults to "16".
3. ***player***: Str. A long string made up of 243 digits (all numbers, between 0 and 5 inclusive) that dictate what the robot will do given a very specific scenario. Defaults to a slightly less dumb human designed robot gene.
4. ***foodperc***: Int. The amount of food pieces (as a percentage out of 100% of all squares on the field) to be scattered randomly across the field. Defaults to "30".
5. ***turnLim***: Int. Specifies the number of turns to allow the simulation to run to. Defaults to "100".
6. ***toPrint***: Bool. Specifies if you want the function to print the map at every turn (basically a viewer for the robot's actions throughout 1 simulation). Defaults to "False".

### The Setup and Rules
1. The robot can do one of 6 actions. These are encoded in its gene.  
	  * 0 = North move  
	  * 1 = East move  
	  * 2 = South move  
	  * 3 = West move  
	  * 4 = Center stay  
	  * 5 = Center eat (incurs a time penalty)  
2. The robot's gene is 243 digits long. It prescribes every possible scenario (3 possibilities ^ 5 tiles) that the robot can face. 
	* A robot's field of view is limited to 5 tiles: 4 cardinal directions (North, East, South, West in order) and center. 
	* Each tile is symbolized: *0* refers to empty, *1* refers to a tile with food, *2* refers to a tile with a wall.
	* The simulator checks the surroundings of the robot at every turn. Say, the robot is in the below position currently. It is described to be the base 3 situation '00121' which, in base 10 numbers, refers to 16. Thus the robot will perform the 16th digit of its gene as an action.  
	```
	 |_|   
	W|F|_  
	 |F|  
	
	==> N:0, E:0, S:1, W:2, C:1  
	==> 00121: base 3 int  
	==> 16: base 10 int  
	==> 16th digit of gene read
	```
3. The only way to win a point is if the robot chooses to eat when it is on a food tile. The simulator will turn that tile empty.
4. The simulator deducts points in these situations:
	* The robot is **against a wall** and tries to **run into it**. 
	* The robot is on an **empty tile** and tries to **eat food**.
	* The robot **stays at the same spot** (i.e. it chooses action 4)
5. The simulator will not allow the robot to move into a wall. The robot will merely stay at its current location.


## Framework/API
* The API rests entirely in the file "Gamev2.py". 
* **Dependencies**: *random, os, pickle, time* and *datetime*. Reasons for each are explained in the file.
* **Functions**: *runGame, generate_field, play* and *print_field*.
* **runGame** is the main function. It takes in the parameters specified [above](*the-environment-and-premise) and runs the simulation using the other functions. 

### Using the API:
1. Command-line example "[tester.bat](tester.bat)". I use this option to see what any interesting gene is doing on the field. 
```batch
python -c "from Gamev2 import runGame; runGame(player='...', seed=967, toPrint=True)"
pause
```
2. Used as .py module example "[evov2.py](evov2.py)". I use this option to run my evolution algorithm like a "manager" script. 
	``` python
	from Gamev2 import runGame
	myscore = runGame(player=myGene, size=5, seed=5435)
	print("My gene scored: " + myscore)
	```

***This is all you need to know if you are building your own algorithm.***
## My evolutionary algorithm
### Key Features are
1. Evolution [evov2.py](evov2.py)
	* gene-pool size
	* mutation
	* perc of top old genes to keep in next generation (*oldvsnew*)
	* number of children each parent-couple can make (*percChild*)
	* effect of 1 point difference on becoming a parent (*inequity*)
	* crossover
	* Dynamically varying seed based on whether the genes will be able to handle a new seed
2. Record-keeping [evov2.py](evov2.py)
	* JSON-creation for genes that beat a overall highscore to set a new best
	* CSV-creation of evolution status at every *x* generations, records current-generation highscore, seed, and evolution parameters
	* Can resume progress given the above JSON and CSV files
3. Display progress in graphs [zzplotme.py](zzplotme.py).
