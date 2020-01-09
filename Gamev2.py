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


import random   # for generating random starting position and field
import os       # for accessing pickle file and 'cls' command for printing
import pickle   # to read pickle files and retrieve field
import time     # to sleep 0.5s after each turn if printing

from datetime import datetime # for testing speed of code


## Concrete Read-only vars
humanbot = '154354054254254254354354054154154154154154254154354154254354224254254224354354004054354054254254054054354054154154054154154054154354054054054004254254254354354054154354154124254254114114114154154154254254154114114114254354224254354254224224224'
defaultseed = 711
defaultsize = 16
defaultfoodperc = 30
defaultTL = 100
storeFile = 'cache.pkl'

def runGame(player=humanbot, seed=defaultseed, size=defaultsize, foodperc=defaultfoodperc, pickling=False, turnLim=defaultTL, toPrint=False):

    # Warn if using default
    if player == humanbot and toPrint: 
        print("Default player (humanbot) used.\n")

    if seed == defaultseed and toPrint: 
        print("Default seed {} used\n".format(defaultseed))

    if size == defaultsize and toPrint:
        print("Default size {} used\n".format(defaultsize))
    
    # I predict defaultTL will be used q often so.. no need to print that
    if toPrint:
        print("Pickling is <<{}>>\n".format('ON' if pickling else 'OFF'))
    
    # Unit Tests for input variables
    assert(len(player) == 243), "\n Player gene length is wrong: {} but correct is 243\n".format(len(player))
    assert('6' not in player and '7' not in player and '8' not in player and '9' not in player), "\n Player gene contains one or many of '6,7,8,9'. Gene is {}".format(player)

    assert(foodperc <= 100 and foodperc>=0), "foodperc is out of bounds: is {}, but correct range is 0-100".format(foodperc)

    # Step 1: Generate the field based on input seed, size and foodperc
    field = generate_field(seed, size, foodperc, pickling)
        
    # INFORMATION OF DATA TYPES
        # field is a list of lists of integers, 0, 1, 2
        # player is a 243-char long string
        # seed, foodperc, size, turn, score are all integers
        # pickling is a boolean

    # Step 2: Play using generated/retrieved field and input player gene
    turn = 0
    score = 0
    currPos = None
    while(turn <= turnLim):
        
        (score, turn, currPos, field) = play(player, field, size, turn, score, seed, currPos)
        
        if toPrint:
            os.system('cls')
            print("Turn", turn, "Score", score)
            print_field(field,currPos)
            print("\n\n")
            time.sleep(0.5)
    
    # Step 3: return score if we are in non-console mode: i.e. not printing.
    if not toPrint:
        return [player,score]

def generate_field(seed, size, foodperc, pickling):
    if pickling:
        if os.path.exists(storeFile):
            cachefile = open(storeFile, "rb")
            data = pickle.load(cachefile)
            cachefile.close()
            if int(data['seed']) == seed and int(data['size']) == size and int(data['foodperc']) == foodperc:
                return data['field']
    
    field = [[2 for i in range(size+2)] for j in range(size+2)]
    random.seed(seed)
    non_wall_field = random.choices(population = [0,1], k = (size)*(size), weights= [100-foodperc, foodperc])
    row = 1 # row 0 is the first layer of walls
    col = 1 # col 0 is wall
    for num in non_wall_field:
        field[row][col] = num
        if col == size:
            col = 1
            row += 1
        else:
            col += 1
    
    if pickling:
        cachefile = open(storeFile, "wb")
        data = {}
        data['seed'] = seed
        data['size'] = size 
        data['foodperc'] = foodperc
        data['field'] = field
        pickle.dump(data, cachefile)
        cachefile.close()
    return field    

def play(player, field, size, turn, score, seed, currPos):

    # returns new field, turn, score, and currPos

    if turn == 0: 
        # Place robot randomly
        random.seed(seed)
        currPos = [random.randint(1,size), random.randint(1,size)]
    currRow = currPos[0]
    currCol = currPos[1]

    surround = [
        field[currRow-1][currCol], # north
        field[currRow][currCol+1], # east
        field[currRow+1][currCol], # south
        field[currRow][currCol-1], # west
        field[currRow][currCol] # center
    ]
    # surround is a list of ints, ordered in a specific fashion

    strSurround = "".join(str(x) for x in surround)
    action = player[int(strSurround, base=3)]
    newPos = [
        [currRow - 1,   currCol  ],     # north move
        [currRow    ,   currCol+1],     # east move
        [currRow + 1,   currCol  ],     # south move
        [currRow    ,   currCol-1],     # west move
        [currRow    ,   currCol  ],     # center stay
        [currRow    ,   currCol  ]      # center eat
    ]
    # newPos is a list of lists of ints indicating row and column of each new possible direction

    action = int(action)
    newPos = newPos[action]
    
    # Give point if bot tried to eat food legally
    if surround[4] == 1 and action == 5:
        score += 1
        field[currRow][currCol] = 0

    # Minus point for pushing against a wall
    elif field[newPos[0]][newPos[1]] == 2:
        score -= 1
    
    # Minus point for staying at same spot
    elif newPos == currPos:
        score -= 1
    
    # Minus point for eating when there is no food available
    elif action == 5 and surround[4] == 0:
        score -= 1
    
    # Move the bot if it is a legal move (i.e. not against a wall)
    elif field[newPos[0]][newPos[1]] != 2:
        currPos = newPos

    ## Prepare vars to be returned
    turn += 1

    return (score, turn, currPos, field)

def print_field (field, currPos):
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

# for console-based testing
# runGame(toPrint=True)


# Time testing code

# loops = 100000
# avgloops = 100
# startTime = datetime.now()

# seed = 711
# pickling = True

# for i in range(loops):
#     runGame(pickling=pickling, seed=seed)
# print("Pickling: {}\nRan {} overall loops\nTime taken for {} loops on avg: {}".format(pickling,loops,avgloops,(datetime.now()-startTime)/(loops/avgloops)))