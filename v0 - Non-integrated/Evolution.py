import random
from subprocess import Popen, PIPE
import multiprocessing as mp
import os
import gc

# Permanent Variables
npool = 40
mutations = 5 # max number of gene mutations in every child, actual mutations is randomly selected below this, x < 243
GameAPIFile = "Game.py"
oldvsnew = 0  # Fraction of gene pool that is the best of the older generation
inequity = 40 # how many times more successful is 1 point lead in making offspring? 0 < x 
percChild = 0.2 # if successful in finding mate, how many children to produce as a fraction of remaining space?
outFile = "zresults.txt"
scoreFile = "zscoresv2.csv"
highscorefile = "zhighscore.txt"
settingsfile = "zsettings.txt"
maxreps = 0
writefreq = 5 # a score save is written at every x generations to save space and make more concise.
newseedfreq = 2 # seed changed every x generations to ensure robots are good at multitude of tasks. Set 0 to never change seed.
size = 16 # size of the board to play on.

# Temporary/Calculated Variables
gen = 0
turnLim = 10 # min number of turns each robot gets at playing
seed = random.randint(0,999999)

def runGame (gene):
    ## use this gene through Popen running an instance of Game.py
    global seed
    proc = Popen(["python", GameAPIFile, "-s", str(seed),"-p", str(gene), "-tl", str(turnLim), "-si", str(size)],stdout=PIPE)
    return (gene,int(proc.communicate()[0]))

def multi_run_manager (genes):
    ## REMEMBER TO check if __name__ == __main__ somewhere!!! else it will run multiple times. Check at outermost function call level.

    p = mp.Pool(int(mp.cpu_count()))
    result = p.map(runGame, genes)
    p.close()
    p.join()
    return result

def write_txt (results, gen, overHigh, currHigh, currAvg):
    f = open(outFile, "w+")
    f.write("Generation {}\nOverall Highscore: {}\nCurrent Generation Highscore: {}\n\n". format(gen, round(overHigh-1), round(currHigh-1,3)))
    f.write("\n".join(str(x[0])+","+str(x[1]) for x in results))
    f.close()
    
    if os.path.exists(scoreFile):
        f1 = open(scoreFile, "a")
        
    else:
        f1 = open(scoreFile, "a")
        f1.write("Generation" +","+ "Current Average" +","+ "Current High"+","+"Size"+","+"TurnLim"+","+"Mutations"+","+"newseedfreq"+","+"Inequity"+","+"oldvsnew"+","+"percChild\n")

    f1.write(str(gen)+","+str(currAvg)+","+str(currHigh)+","+str(size)+","+str(turnLim)+","+str(mutations)+","+str(newseedfreq)+","+str(inequity)+","+str(oldvsnew)+","+str(percChild)+"\n")
    f1.close()

def crossover(p1, p2, nChildren):
    children = []
    for i in range(nChildren):
        breakpt = random.randint(0,242)
        child = p1[:breakpt]+p2[breakpt:]

        mymut = int(random.random()*mutations)
        for mut in range(mymut):
            mutpt = random.randint(0,242)
            child = child[:mutpt] + random.choice(['0','1','2','3','5']) + child[(mutpt+1):]
        
        children.append(child)
    return children

def selection (results):
    newGenes = []

    # add in the best of the old generation according to fraction specified earlier
    for i in range(round(oldvsnew*npool)):
        newGenes.append(results[i][0])
    
    offset = min(results, key=lambda x: x[1])[1]
    counts = [int((x[1]-offset+1)*inequity) for x in results]
    population = [x[0] for x in results]
    results = [x for x,count in zip(population, counts) for i in range(count)]
    currParents = random.sample(results, k = npool)
    nChildren = round(percChild*npool)
    # fill up the rest of the space with offspring, with equality specified earlier
    while len(newGenes) < npool and len(currParents) > 1:
        if npool - len(newGenes) < nChildren:
            nChildren  = npool - len(newGenes)
        if currParents[0] == currParents[1]:
            del(currParents[0])
        else:
            
            newGenes.extend(crossover(currParents[0],currParents[1], nChildren))
            del(currParents[0])
    return newGenes    

def evolution_manager():
    genes = []
    global seed
    global turnLim
    overallHigh = 0
    currentHigh = 0
    gen = 0
    
    while len(genes) < npool:
        if os.path.exists(outFile):
            f = open(outFile, "r")
            data = f.readlines()
            gen = int(data[0][11:].strip()) + 1
            overallHigh = int(data[1][-2:].strip())
            del(data[0:5])
            data = map(lambda s: s[:243].strip(), data)
            genes.extend(data)
            data = []
            f.close()
            break
        else:
            ## Create everyone or top up randomness
            genes.append("".join(x for x in random.choices(population=['0','1','2','3','4','5'], k = 243)))
    
    running = True
    while running:
        gc.collect()
        genes = multi_run_manager(genes)
        genes = sorted(genes, key=lambda x: x[1],reverse=True)
        currentHigh = genes[0][1]
        if currentHigh >= overallHigh:
            overallHigh = currentHigh
            if not os.path.exists(highscorefile):
                f = open(highscorefile, "a")
                f.write("Score, Seed, Gene\n")
            else:
                f = open(highscorefile,"a")
            
            f.write("{}, {}, {}\n".format(str(genes[0][1]), seed,str(genes[0][0])))
            f.close()    
        currAvg = round(sum(x[1] for x in genes)/len(genes),3)
        print("___________________________________")
        print("Genepool size: {}, Seed: {}, Max Turns: {}".format(len(genes), seed, turnLim))
        print("Generation {} \nOverall Highscore: {} \nCurrent Gen Highscore: {}\nCurrent Gen Avg:{}". format(gen, round(overallHigh-1,2), round(currentHigh-1,2), round(currAvg-1,2)))
        
        if gen % writefreq == 0 and gen != 0:
            write_txt(genes, gen, overallHigh, currentHigh, currAvg)
        var_changer()

        genes = selection(genes)
        if newseedfreq != 0:
            if gen % newseedfreq == 0:
                random.seed(seed)
                seed = random.randint(0,999999)
                print("New seed chosen: {}".format(seed))
        gen += 1
        
        if maxreps !=0 and maxreps == gen:
            running = False

def var_changer():
    global newseedfreq
    global mutations
    global inequity
    global percChild
    global oldvsnew
    global turnLim
    global size
   
    if os.path.exists(settingsfile):
        f = open(settingsfile,'r')
        data = f.readlines()
        tempvars = []
        for line in data:
            line = line.split(" = ")
            tempvars.append(float(line[1]))
        mutations = int(tempvars[0])
        oldvsnew = tempvars[1]
        inequity = tempvars[2]
        percChild = tempvars[3]
        newseedfreq = int(tempvars[4])
        turnLim = int(tempvars[5])
        size = int(tempvars[6])
    return

if __name__ == '__main__':
    evolution_manager()