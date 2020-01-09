from msvcrt import getch
from os import system
import baseconvert

def keyCheck ():
    while True:
        key = ord(getch())
        print(key)
        if key == 72:
            return "0"
        if key == 80:
            return "2"
        if key == 75:
            return "3"
        if key == 77:
            return "1"
        if key == 101:
            return "5"

def makeBot():
    gene = []
    for i in range(243):
        # Clear the screen
        system('cls') 

        #draw the situation
        currSit = baseconvert.base(str(i), 10, 3, string=True)
        currSit = str(currSit)
        while len(currSit) < 5:
            currSit = "0" + currSit
        
        if currSit[4] == "2":
            gene.append("4")
            continue

        print(currSit)
        sitPrint(currSit)
        print("Press arrow keys or the 'E' key to program the robot and move to the next scenario.")
        gene.append(keyCheck())
    print("".join(gene))

def sitPrint (sit):
    sit = str(sit)
    wordSit = []
    for i in range(len(sit)):
        if sit[i] == '0':
            wordSit.append('-')
        if sit[i] == '1':
            wordSit.append('F')
        if sit[i] == '2':
            wordSit.append('#')
    
    print("\t  {}\n\t{} {} {}\n\t  {}".format(
        wordSit[0], 
        wordSit[3], 
        wordSit[4],
        wordSit[1],
        wordSit[2]))

makeBot()

# 154354054254254254354354054154154154154154254154354154254354224254254224354354004054354054254254054054354054154154054154154054154354054054054004254254254354354054154354154124254254114114114154154154254254154114114114254354224254354254224224224