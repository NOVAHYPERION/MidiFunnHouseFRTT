# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:40:42 2019

@author: Leonardo
"""


def ReadMidNoteData(directory):
    '''Give exact directory, with file name (with .txt)
     Will return note information note lowest note (index 0), average note (index 1), Highest Note (index 2)'''
    if(directory[-4:] != ".txt"):
        assert("ERROR: Not a text file.")
        return -1
    fi = open(directory)
    first = True
    lastVals = []
    avgallnotes = []
    allnotes = []
    allnotesum = 0
    notesoftrack = []
    avgnotesoftrack= []
    notesoftracksum = 0
    note = 0
    for i in fi:
        liner = i.split(", ")
        if(first):
            lastVals.append(int(liner[0]))
            lastVals.append(int(liner[0]))
            first = False
        else:
            lastVals[0],lastVals[1] = lastVals[1],lastVals[0]
            lastVals[1] = liner[0]
        if(lastVals[0] != lastVals[1]):
            if(notesoftracksum != 0):
                avgnotesoftrack.append((notesoftracksum // len(notesoftrack)))
                notesoftracksum = 0
                notesoftrack = []
        if (len(liner) == 6):
            if( liner[2][:4] == "Note"):
                note = int(liner[4])
                allnotes.append(int(liner[4]))
                notesoftrack.append(int(liner[4]))
                notesoftracksum +=  note
                allnotesum += note
    avgallnotes.append(min(allnotes))
    avgallnotes.append(allnotesum // len(allnotes))
    avgallnotes.append(max(allnotes))
    fi.close()
    return avgallnotes

def RandMidTimingData(directory):
    '''Give exact directory, with file name (with .txt)
    Will return the shortest amount of time between each note (index 0), average time (index 1), longest time (index 2).'''
    if(directory[-4:] != ".txt"):
        assert("ERROR: Not a text file.")
        return -1
    fi = open(directory)
    first = True
    retval = []
    twenotes = []
    alltwenotes = 0
    twenotesall = 0
    totalsum = 0
    alldiffs = []
    lastVals = []
    timernchan = []
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
        if(first):
            lastVals.append(int(liner[0]))
            lastVals.append(int(liner[0]))
            first = False
        else:
            lastVals[0],lastVals[1] = lastVals[1],lastVals[0]
            lastVals[1] = liner[0]
        if(len(liner) == 6):
            #make sure the line is a note line. 
            if( liner[2] == "Note_on_c"):
                timernchan.append((liner[1],liner[3]))
                if(len(timernchan) > 1 ):
                    tweenotes = int(liner[1]) - int(timernchan[-2][0])
                    twenotesall += tweenotes
                    twenotes.append(tweenotes)
                    alltwenotes += 1
            elif( liner[2] == "Note_off_c"):
                for chan in range(len(timernchan)):
                    if timernchan[chan][1] == liner[3]:
                        diff = int(liner[1]) - int(timernchan[chan][0])
                        alldiffs.append(diff)
                        totalsum += diff
                        break
    retval = [min(twenotes), twenotesall // alltwenotes, max(twenotes)]
    fi.close()
    return retval
