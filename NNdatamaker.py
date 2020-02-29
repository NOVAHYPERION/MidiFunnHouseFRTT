# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:04:32 2019

@author: Leonardo
"""
import os
import random
import shutil as sh

def NNData(filename):
    '''Enter a csv file, output a csv file that you can use for the NN.'''
    if(filename[-4:] != ".txt"):
        assert("ERROR: Not a text file.")
        return -1
    ocwd = os.getcwd()
    cwd = ocwd + "\\Midicsv\\" + filename
    outname = filename[:-4] + str(random.randint(0,100000))+".txt"
    outdir = ocwd + "\\NNdata\\" + outname
    fi = open(cwd)
    twenotes = []
    alltwenotes = 0
    twenotesall = 0
    totalsum = 0
    alldiffs = []
    lastVals = [0,0]
    timernchan = []
    rando = open(outdir,"w")
    for i in fi:
        #split the line into its bits
        #(0 is track number, 1 is tick time, 
        #2 is command, 3 is channel, 
        #4 is note, 5 is volume)
        liner = i.split(", ")
        if liner[2] == "Start_track\n" and len(lastVals) == 2:
            lastVals[0] = 0
            lastVals[1] = 0 
            timernchan = []
        else:
            lastVals[0],lastVals[1] = lastVals[1],lastVals[0]
            lastVals[1] = liner[0]
        if(len(liner) == 6):
            #make sure the line is a note line. 
            if(liner[2] == "Note_on_c" and liner[5] != "0\n") :
                timernchan.append([int(liner[1]),int(liner[3]),liner[4]])
                if(len(timernchan) > 1 ):
                    tweenotes = int(liner[1]) - timernchan[-2][0]
                    twenotesall += tweenotes
                    twenotes.append(tweenotes)
                    alltwenotes += 1
            elif( liner[2] == "Note_off_c" or (liner[2] == "Note_on_c" and liner[5] == "0\n")):
                for chan in range(len(timernchan)):
                    if str(timernchan[chan][1]) == liner[3]:
                        diff = int(liner[1]) - timernchan[chan][0]
                        rando.write(str(timernchan[chan][0]) + ", " + str(liner[1]) + ", " + str(diff) + ", " + liner[4]+ "\n" )
                        alldiffs.append(diff)
                        totalsum += diff
                        del timernchan[chan]
                        break
    
    fi.close()
    rando.close()
    return outname

#NNData("deb_clai.txt")

def NNdatamaker(direc,outdirec):
    '''This was going to be like a super recursive go through every single csv
    file and make all the NNdata stuff, but it seemed too... static for me to do that
    so I figured I'd wait until I knew exactly what hyperparameters I'd be using.
    Will be implemented and used later, probably.'''
    listostuff = os.listdir(direc)
    path_to_dir = (outdirec)
    garbage = []
    try:
        os.mkdir((path_to_dir))
    except(FileExistsError):
        print("file already exists")
    converts = 0
    for j in listostuff:
        currDir = direc+"\\"+j
        #(If this is another directory, do it again)
        if(os.path.isdir(currDir) and (j != ".git")):
            print(currDir)
            converts += RecMidiChatty(currDir,(path_to_dir + "\\" + j))
        elif (j[-4:] != '.mid'):
            continue
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    