# -*- coding: utf-8 -*-
"""
Created on Fri May 31 16:25:55 2019

@author: Leonardo Lamboglia
"""
import py_midicsv
import shutil
import os
from datetime import datetime

'''with open("Lullaby1.txt", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(row)'''
        
'0, 0, Header, 1, 3, 256'
'1, 0, Start_track'
'1, 0, Time_signature, 4, 2, 24, 8'
def genMidiSamp(txt,add=""):
    pathTo = os.getcwd()
    now = datetime.now() # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hours = now.strftime("%H")
    mins = now.strftime("%M")
    seconds = now.strftime("%S")
    fullStr= year+month+day+hours+ mins +seconds
    NewFileName = add+fullStr+".txt"
    CreateText = open(NewFileName,'w')
    CreateText.write('0, 0, Header, 1, 3, 256\n')
    CreateText.write('1, 0, Start_track\n')
    CreateText.write('1, 0, Time_signature, 4, 2, 24, 8\n')
    BasisText = open(txt,'r')
    darp = 400
    for i in BasisText:
        if(i=="\n"):
            break
        CreateText.write('1, '+str(darp)+', Note_on_c, 15, '+i[:-1]+', 100\n')
        darp += 100
    darp += 5000
    CreateText.write('1, '+ str(darp) +', End_track\n')
    CreateText.write('0, 0, End_of_file')
    CreateText.close()
    BasisText.close()
    start = pathTo + "\\" + NewFileName
    end = pathTo + "\\randoTxt"
    shutil.move(start,end)
    return (end + "\\"+NewFileName)
    
    
def txttomidi(txt):
    pathTo = os.getcwd()
    outFile = txt[0:-4] + ".mid"
    actualVal = outFile.split("\\")[-1]
    midi_object = py_midicsv.csv_to_midi(txt)
    with open(outFile, "wb") as output_file:
        midi_writer = py_midicsv.FileWriter(output_file)
        midi_writer.write(midi_object)
    start = pathTo + "\\randoTxt\\"+ actualVal
    end = pathTo + "\\randoMidi"
    shutil.move(start,end)

def miditotxt(direc):
    csvText = py_midicsv.midi_to_csv(direc)
    outDirec = direc.split("\\")
    outval = outDirec[-1][0:-4]
    CreateText = open(outval+".txt",'w')
    for i in csvText:
        CreateText.write(i)
    CreateText.close()
    
#miditotxt(r"C:\Users\David\Desktop\NN\Bwv001- 400 Chorales\deb_clai.mid")

