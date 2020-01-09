import os       # to open all files: settings, results, etc
import json     # to read the results file and resume the game
import random   # To generate gene pool from scratch
import multiprocessing as mp # To split running simulation across all CPU cores


import Gamev2 as GameAPI # Actual game functions to run each gene

# Concrete read-only variables
settingsfile = "zsettings.txt"
outfile = "zresults.json"
highscorefile = "zhighscores.txt"
scorefile = "zscoresv2.csv"
defaultnpool = 40
maxgens = 0


def evov2(npool=defaultnpool):
    
    # Step 0: Initialize empty variables
    genes = []
    gen = 0
    overallHigh = 0
    currentHigh = 0
    seed = random.randint(0,999999)
    foodperc = 30
    pickling = False
    writefreq = 50

    # Step 1: Start the actual simulations
    running = True
    if maxgens !=0 and maxgens <= gen:
        running = False 
    
    scoretobeat = 5
    gensincebeat = 0
    initialise = True
    while running:

        if initialise:
            initialise = False
            # Step 1: Determine initial variables to use, via var_changer()
            (mutations, oldvsnew, inequity, percChild, newseedfreq, turnlim, size, writefreq) = var_changer(settingsfile)

            # Step 2: Initialise the gene pool
            if os.path.exists(outfile):
                f = open(outfile, "r")
                data = json.load(f)
                f.close()
                
                # Use the retrieved dict to repopulate and resume
                storedResults = data['genes']
                genes.extend([result[0] for result in storedResults])
                gen = int(data['gen'])
                overallHigh = int(data['overallHigh'])
            
            if len(genes) < npool:
                while len(genes) < npool:
                    ## Create everyone or top up randomness
                    genes.append("".join(x for x in random.choices(population=['0','1','2','3','4','5'], k = 243)))
            elif len(genes) > npool:
            	while len(genes) > npool:
            		del(genes[-1])
        
        resultgenes = []
        # Step 3a: run the actual genepool through the simulations
        resultgenes = multi_run_manager(genes, seed, size, foodperc, pickling, turnlim)

        # 3b: Sort the results [(gene, score),...] by scores
        resultgenes = sorted(resultgenes, key=lambda x: x[1],reverse=True)
        currentHigh = resultgenes[0][1]

        # 3c: Overwrite overallHigh if need be and write to highscorefile too
        if currentHigh > overallHigh:
            overallHigh = currentHigh
            if not os.path.exists(highscorefile):
                f = open(highscorefile, "a")
                f.write("Score, Seed, Gene\n")
            else:
                f = open(highscorefile,"a")
            f.write("{}, {}, {}\n".format(str(resultgenes[0][1]), seed,str(resultgenes[0][0])))
            f.close()
        
        # Step 4: Calculate Current Average score and print to console
        currAvg = round(sum(x[1] for x in resultgenes)/len(resultgenes),3)
        print("___________________________________")
        print("Genepool size: {}, Seed: {}, Max Turns: {}".format(len(genes), seed, turnlim))
        print("Score to beat: {}, Gens since score beat: {}".format(scoretobeat, gensincebeat))
        print("Generation {} \nOverall Highscore: {} \nCurrent Gen Highscore: {}\nCurrent Gen Avg:{}". format(gen, overallHigh, currentHigh, round(currAvg,3)))

        # Step 5: check if need to write progress to file
        if gen % writefreq == 0 and gen != 0:
            write_JSON(resultgenes, gen, overallHigh, currentHigh, currAvg, size, turnlim, mutations, newseedfreq, inequity, oldvsnew, percChild, scoretobeat)
        # Step 6: run var_changer() again in case things changed for the next turn
        (mutations, oldvsnew, inequity, percChild, newseedfreq, turnlim, size, writefreq) = var_changer(settingsfile)
        
        # Step 7: Select the next generation
        genes = selection(resultgenes, oldvsnew, inequity, mutations, percChild)
        if newseedfreq != 0:
            if gen % newseedfreq == 0:
                random.seed(seed)
                seed = random.randint(0,999999)
                print("New seed chosen: {}".format(seed))
        else:
            if currentHigh >= scoretobeat or gensincebeat >= 100*scoretobeat:
                gensincebeat = 0
                random.seed(seed)
                seed = random.randint(0,999999)
                print("New seed chosen: {}".format(seed))
                if currentHigh >= scoretobeat:
                	scoretobeat += 1
        gen += 1
        gensincebeat += 1
        
        if maxgens !=0 and maxgens <= gen:
            running = False 


def var_changer(settingsfile):
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
        writefreq = int(tempvars[7])
    return (mutations, oldvsnew, inequity, percChild,newseedfreq, turnLim, size, writefreq)
def multi_run_manager(genepool, seed, size, foodperc, pickling, turnLim):
    # genepool is a list of strings of length 243
    # this function must be run only after checking if __name__ == __main__. 

    argList = []
    for gene in genepool:
        argList.append((str(gene), seed, size, foodperc, pickling, turnLim))
    
    p = mp.Pool(int(mp.cpu_count()))
    result = p.starmap(GameAPI.runGame, argList)
    p.close()
    p.join()  
    return result

def write_JSON (results, gen, overHigh, currHigh, currAvg, size, turnLim, mutations, newseedfreq, inequity, oldvsnew, percChild, scoretobeat):
    f = open(outfile, "w+")
    toWrite = {}
    toWrite['gen'] = gen
    toWrite['overallHigh'] = overHigh
    toWrite['genes'] = results
    json.dump(toWrite, f)
    f.close()
    
    if os.path.exists(scorefile):
        f1 = open(scorefile, "a")
        
    else:
        f1 = open(scorefile, "a")
        f1.write("Generation" +","+ "Current Average" +","+ "Current High"+","+"Size"+","+"TurnLim"+","+"Mutations"+","+"newseedfreq"+","+"Inequity"+","+"oldvsnew"+","+"percChild"+","+"Score To Beat\n")

    f1.write(str(gen)+","+str(currAvg)+","+str(currHigh)+","+str(size)+","+str(turnLim)+","+str(mutations)+","+str(newseedfreq)+","+str(inequity)+","+str(oldvsnew)+","+str(percChild)+","+str(scoretobeat)+"\n")
    f1.close()

def selection (results, oldvsnew, inequity, mutations, percChild):
    newGenes = []
    npool = len(results)

    # add in the best of the old generation according to fraction specified earlier
    for i in range(round(oldvsnew*npool)):
        newGenes.append(results[i][0])
    
    offset = min(results, key=lambda x: x[1])[1]-2
    counts = [int((x[1]-offset)*inequity) for x in results]
    population = [x[0] for x in results]
    results = [x for x,count in zip(population, counts) for i in range(count)]
    currParents = random.sample(results, k = npool)

    # fill up the rest of the space with offspring, with equality specified earlier
    while len(newGenes) < npool:
        nChildren = round(percChild*(npool-len(newGenes)))+1
        newGenes.extend(crossover(currParents[0],currParents[1], nChildren, mutations))
        del(currParents[0])
        
    return newGenes    

def crossover(p1, p2, nChildren, mutations):
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

if __name__ == '__main__':
    evov2()