# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:39:00 2019

@author: Leo
"""
import py_midicsv as pym
import os
import shutil as sh
import random

def RecMidiChatty(direc,outdirec):
    '''Give me a directory, I'll convert all the midi files into csv's, and put them into the outdirec!
    (I'll do my best to make it an exact copy, inner folders and all)
    This is also the Chatty version! I'll be printing out a bunch of stuff. If you don't want that just do RecMidi.'''
    listostuff = os.listdir(direc)
    print(listostuff)
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
        else:
            print(j)
            try:
                csvText = pym.midi_to_csv(currDir)
            except(TypeError):
                print("ERROR ERROR ERROR\nType Error! " + j + " won't be converted! File just sucks probably.")
                continue
            except:
                print("ERROR ERROR ERROR\n Something went wrong! " + j + " won't be converted!!!!!")
                continue
            mani = j[:-4]
            mani+=".txt"
            CreateText = open(direc+"\\"+mani,'w+')
            for i in csvText:
                try:
                    CreateText.write(i)
                except:
                    print("ERROR\n Something went wrong when writing. Adding to the pile...")
                    CreateText.close()
                    garbage.append(path_to_dir+"\\"+mani)
                    break
            CreateText.close()
            path_to_curr = direc + "\\" +mani
            try:
                sh.move(path_to_curr,path_to_dir)
            except:
                renameVal = path_to_curr[:-4]+str(converts)+".txt"
                os.rename(path_to_curr,renameVal)
                sh.move(renameVal,path_to_dir)
            converts +=1
    for i in garbage:
        os.remove(i)
    return converts

#print(RecMidiChatty(r"C:\Users\David\Desktop\Midifun\130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]2\130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]",r"C:\Users\David\Desktop\NN\Midicsv"))

