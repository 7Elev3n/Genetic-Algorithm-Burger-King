# This is the API that will run the game given a player code. Each code will dictate what the robot will do:
# At every frame, a robot is given a state of its surroundings, an int of 5 digits. 
#### North, East, South, West, Center. 
#### Each can be one of three things:
#### 0 = Empty
#### 1 = Food
#### 2 = Wall
# So there are 3^5 = 243 possibilities. Each player's gene length should be 243 digits long. 

# Player specifications:
# 243 digit long STRING. 
# Each digit must be either:
#### 0 = North move
#### 1 = East move
#### 2 = South move
#### 3 = West move
#### 4 = Center stay
#### 5 = Center eat (incurs a time penalty )

# Ordering of gene:
# 00000 -> 00001 -> 00002 -> 00010 -> 00011 -> 00012 -> ...

# Inputs into the Game. (*) indicates mandatory.
# -player or -p     = Player gene (*), must be 243 digits
# -seed or -s       = Random seed to use if any < 100000. Default is 711
# -foodperc or -fp  = Percentage of food of all the tiles, between 0 and 100. Default is 30. 
# -size or -si      = Size of the board (excluding walls). The field is a square grid. Default is 16.


# Imports
import sys
import random
import time
from os import system

# Permanent Variables
seedrange = [0,1000000]
sizerange = [5,32]
foodperc = 0.3
turnLim = 100

# Calculated Permanent variables
seed = 711
player = "".join(x for x in random.choices(population=['0','1','2','3','4','5'], k = 243)) 
size =  10# Square grid of side length
field = []
toPrint = False

# Temporary Variables
turn = 0
currPos = [0,0]
score = 1

def initialise ():
    for i,cmd in enumerate(sys.argv):
        if cmd == "-seed" or cmd == "-s":
            global seed
            if i+2 < len(sys.argv) :
                assert ("-" in str(sys.argv[i+2])), "\nGame Error: {} flag was given more than 1 argument.".format(cmd)
            assert(int(sys.argv[i+1]) <= seedrange[1]), "\nGame Error: Seed argument is out of range ({} not between {} and {})".format(sys.argv[i+1], seedrange[0], seedrange[1])
            
            
            seed = int(sys.argv[i+1])

        if (cmd == "-player" or cmd == "-p"):
            global player
            if i+2 < len(sys.argv) :
                assert ("-" in str(sys.argv[i+2])), "\nGame Error: {} flag was given more than 1 argument.".format(cmd)
            
            assert (len(sys.argv[i+1]) == 243), "\nGame Error: Player gene length is {} (should be 243, see instructions)".format(len(sys.argv[i+1]))

            
            player = sys.argv[i+1]

        if (cmd == "-size" or cmd == "-si"):
            global size
            assert (int(sys.argv[i+1]) > sizerange[0] and int(sys.argv[i+1]) < sizerange[1]), "\nGame Error: Size argument is out of range ({} not between {} and {})".format(sys.argv[i+1], sizerange[0], sizerange[1])

            size = int(sys.argv[i+1])

        if (cmd == "-foodperc" or cmd == "-fp"):
            global foodperc
            assert(int(sys.argv[i+1]) <= 100 and int(sys.argv[i+1]) >= 0), "\nGame Error: Food Percentage is out of bounds. ({} not between {} and {} inclusive)".format(sys.argv[i+1], 0, 100)
            foodperc = int(sys.argv[i+1])/100
        
        if (cmd == "-turnlim" or cmd == "-tl"):
            global turnLim
            assert(int(sys.argv[i+1]) >= 0), "\nGame Error: Turn Limit is out of bounds. ({} not above {})".format(sys.argv[i+1], 0)
            turnLim = int(sys.argv[i+1])
        
        if (cmd == "-print"):
            global toPrint
            toPrint = True

def generate_field ():
    field = [[2 for i in range(size+2)] for j in range(size+2)]
    random.seed(seed)
    non_wall_field = random.choices(population = [0,1], k = (size)*(size), weights= [1-foodperc, foodperc])
    row = 1 # row 0 is the first layer of walls
    col = 1 # col 0 is wall
    for num in non_wall_field:
        field[row][col] = num
        if col == size:
            col = 1
            row += 1
        else:
            col += 1
    return field

def print_field ():
    global currPos
    for row, rowdata in enumerate(field):
        for col, itm in enumerate(rowdata):
            if row == currPos[0] and col == currPos[1]:
                print("X", end=" ")
            else:
                if itm == 0:
                    print(" ",end=" ")
                if itm == 1:
                    print(".",end=" ")
                if itm == 2:
                    print("#",end=" ")
        print()
                

def play ():
    global turn
    global currPos
    global score
    global field

    if turn == 0: 
        # Place robot randomly
        random.seed(seed)
        currPos = [random.randint(1,size), random.randint(1,size)]
    #print(currPos)
    currRow = currPos[0]
    currCol = currPos[1]

    surroundings = [
        field[currRow-1][currCol], # north
        field[currRow][currCol+1], # east
        field[currRow+1][currCol], # south
        field[currRow][currCol-1], # west
        field[currRow][currCol] # center
    ]

    surroundings = "".join(str(x) for x in surroundings)
    action = player[int(surroundings, base=3)]
    #print("Action {} is performed, current food = {}.".format(action,surroundings[4]))
    newPos = [
        [currRow - 1,   currCol  ],     # north
        [currRow    ,   currCol+1],     # east
        [currRow + 1,   currCol  ],     # south
        [currRow    ,   currCol-1],     # west
        [currRow    ,   currCol  ],     # center
        [currRow    ,   currCol  ]      # center
    ]
    
    action = int(action)
    newPos = newPos[action]
    
    if score < 2 and action != 4 and action != 5 and surroundings[4] == 0:
        score += 0
    
    elif action == 5 and surroundings[4] == '1':
        score += 1
        field[currRow][currCol] = 0
    elif action == 5 and surroundings[4] == '0':
        score -= 1
    
    if field[newPos[0]][newPos[1]] != 2:
        currPos = newPos
    else:
        score -= 1
    



def main ():
    global seed
    global player
    global size
    global foodperc
    global field
    global turn
    global score

    initialise()
    assert(len(player) == 243 and size >= sizerange[0] and size <= sizerange[1] and foodperc < size*size), "\nGame Error: Some variable initialised wrongly. Check after initialisation."
    
    field = generate_field()
    #print("Map:")
    #print_field ()
    
    while (turn <= turnLim):
        play()
        turn += 1
        if toPrint:
            system('cls')
            print("Turn", turn, "Score", score)
            print_field()
            print("\n\n")
            time.sleep(0.5)
    
    print("{}".format(score))
main() 
