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
2. The only way to win a point is if the robot chooses to eat when it is on a food tile. 
3. The simulator deducts points in these situations:
	* The robot is **against a wall** and tries to **run into it**. 
	* The robot is on an **empty tile** and tries to **eat food**.
	* The robot **stays at the same spot** (i.e. it chooses action 4)
4. The simulator will not allow the robot to move into a wall. The robot will merely stay at its current location.
5. Once a robot legally and successfully eats a piece of "food" on a tile, the simulator will turn that tile empty and the simulation will continue.

## Framework/API
* The API rests entirely in the file "Gamev2.py". 
* Dependencies: *random, os, pickle, time* and *datetime*. Reasons for each are explained in the file.
* Functions: *runGame, generate_field, play* and *print_field*.
* **runGame** is the main function. It takes in the parameters specified [here in this README](#the-environment-and-premise) and runs the simulation using the other functions. 

### Using the API:
