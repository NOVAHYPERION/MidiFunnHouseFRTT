# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 15:50:01 2019

@author: Leonardo
"""
import random

def RandMidData(directory,outdir, minVal, maxVal):
    ''' give exact directory, out directory (with file name, doesn't need to ), min random val and max random val'''
    if(directory[-4:] != ".txt"):
        assert("ERROR: Not a text file.")
        return -1
    fi = open(directory)
    rando = open(outdir,"w")
    writestring = ""
    for i in fi:
        writestring=""
        liner = i.split(", ")
        if (len(liner) == 6):
            if( liner[2][:4] == "Note"):
                liner[4] = str(random.randint(minVal,maxVal))
        writestring += liner[0]
        for j in range(1,len(liner)):
            writestring += ", " + liner[j]
        rando.write(writestring)
    fi.close()
    rando.close()
        
def RandMidTimingData(directory,outdir, minVal, maxVal):
    ''' give exact directory, out directory (with file name, doesn't need to ), min random val and max random val'''
    if(directory[-4:] != ".txt"):
        assert("ERROR: Not a text file.")
        return -1
    fi = open(directory)
    rando = open(outdir,"w")
    writestring = ""
    lastVals = [0,0]
    switch = False
    prevVal = 0
    for i in fi:
        lastVals[0], lastVals[1] = lastVals[1], lastVals[0]
        writestring= ""
        liner = i.split(", ")
        lastVals[1] = int(liner[1])
        if not(switch) and lastVals[1] != lastVals[0] and liner[2] != "End_track\n":
            switch = True
            prevVal = int(liner[1])
        elif(liner[2] == "Start_track\n"):
            lastVals = [0,0]
            switch = False
        if(switch):
            liner[1] = prevVal + random.randint(minVal, maxVal)
            prevVal = int(liner[1])
        writestring += liner[0]
        for j in range(1,len(liner)):
            writestring += ", " + str(liner[j]) 
        rando.write(writestring)
    fi.close()
    rando.close()

            