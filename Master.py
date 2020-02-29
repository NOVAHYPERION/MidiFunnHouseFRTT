# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:32:16 2019

@author: David
"""
import random
import os
import RandomMaker
import TxtToMidiConvert
import MidiCsvReading
import shutil

CurrenDir = os.listdir()
dovalpre = os.getcwd()
print(CurrenDir)
if(not( "randoTxt" in CurrenDir)):
    os.mkdir(dovalpre + "\\randoTxt")
if(not( "randoMidi" in CurrenDir)):
    os.mkdir(dovalpre + "\\randoMidi")
if(not("Midicsv") in CurrenDir):
    print("Midicsv directory not found. All inputs are now expecting a specific directory.\
          If you convert a midi to a csv, this directory will be automatically created.")

strin = input("Hello! Welcome to the Midi fun house! If you would like to convert a midi2csv, put in a textfile (put the .txt), also make sure this script is in the same directory as a file named Midicsv where the midi file is in.\n")
randoe = random.randint(0,10000000)
print(randoe)

doval = dovalpre + "\\Midicsv\\" + strin
hold = doval.split("\\")
ChooseRando = input("N or T (Notes or Time)\n")
while(not(ChooseRando == "N" or ChooseRando == "T")):
    ChooseRando = input("Try again. N or T")

if(ChooseRando == "N"):
    poor = MidiCsvReading.ReadMidNoteData(doval)
    outer = dovalpre + "\\randoTxt\\" + hold[-1][:-4] + "RandomedNotes" +str(randoe)+".txt"
    RandomMaker.RandMidData(doval,outer,poor[0],poor[2])
    TxtToMidiConvert.txttomidi(outer)

elif(ChooseRando == "T"):
    poor = MidiCsvReading.RandMidTimingData(doval)
    outer = dovalpre + "\\randoTxt\\" + hold[-1][:-4] + "RandomedTimes" +str(randoe)+".txt"
    print(poor[0],poor[1],poor[2])
    RandomMaker.RandMidTimingData(doval,outer,poor[0],poor[1])
    TxtToMidiConvert.txttomidi(outer)
print("All done!")