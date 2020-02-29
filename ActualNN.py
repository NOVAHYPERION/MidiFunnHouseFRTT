# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:54:49 2019

@author: Leonardo Lamboglia
"""
import TxtToMidiConvert as TTM
import NNdatamaker as NND
import seaborn as sns; sns.set() 
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import keras
import shutil
import os
from datetime import datetime
global NNFileName 
'''
Right. So. Here's how it goes. The TxtToMidiConvert will take a midi file and convert it
to the csv file if you need it to be. Then I need to take that csv file and push it through
the NNdatamaker file to get the data that will be used for the NN. That is in the form
Note Start, Note End, Note Duration, Note Note (the actual numeric value of the note).

We don't need to worry about Master.py, that's mostly for an idea I have about making a GAN.

An important note: All of the music right now that is generated has time set to a constant.
This means that every note will be played a set distance away from each other, until
time is added to the NN.
'''

        #
        #
        #If you want to change the file you put into the NN put it here.
        #
'''
Right. So I went ahead and made sure that you can take a csv of a song and push it through
the NNdatamaker right here.
Just make sure wherever you're running this you have a file named "Midicsv" (where the midi csv's are) and
a file named NNdata (where the NNdata will go) wherever you're running it.
'''

NNFileName = NND.NNData('2_14_J_E_N_O_V_A.txt')

global StripName 
StripName = NNFileName[:-4]
        #
        #
        #
        
        
        
def Batch_Gen(dataSet):
    Xvals = []
    Yvals = []
    for i in range(0 ,len(dataSet.columns) -1, 1):
        NoteVal = dataSet[i].tolist()[3]
        Xvals.append(NoteVal)
        Noterized = [0]*127
        Noterized[NoteVal] = 1
        Yvals.append(Noterized)
    return np.array(Xvals), np.array(Yvals)

def chancer(preds,temp = 1.0):
    '''This is for taking the out put of the NN and choosing notes from the output arrays'''
    preds = np.reshape(preds, preds.size)
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temp
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def on_epoch_end(epoch, logs):
    ''' I have it set up so that every 5 epochs it will make a midi file '''
    if((epoch%5 == 0)):
        CWD = os.getcwd()
        now = datetime.now() # current date and time
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hours = now.strftime("%H")
        mins = now.strftime("%M")
        seconds = now.strftime("%S")
        fullStr= year+month+day+hours+ mins +seconds
        FileName = StripName+fullStr + "NNtestmidiEpoch"+str(epoch)+".txt"
        CreateText = open(FileName,'w')
        for i in range(0,126):
            CreateText.write(str(chancer(model.predict(np.array([[[i]]])),.4))+'\n')
        CreateText.write('\n')
        CreateText.close()
        StartP = CWD + "\\" + FileName
        ExactPath = CWD + "\\NNMIDITESTS\\"+ FileName
        shutil.move(StartP,ExactPath)
        TTM.txttomidi(TTM.genMidiSamp(ExactPath,FileName[:-4]))
        
##
        
#set up the On Epoch Ends
MidiMake = keras.callbacks.LambdaCallback(on_epoch_end=on_epoch_end)
#Get NN data
dataset = pd.read_csv(os.getcwd() + r"\\NNdata\\" + NNFileName)
dataset.columns = ["Note Start", "Note End", "Note Duration", "Note Note"]
dataset.sort_values(by=["Note Start"])
dataset = dataset.T

scaler = MinMaxScaler(feature_range=(0, 1))
XValus, YValus = Batch_Gen(dataset)

XValus = np.reshape(XValus,(XValus.shape[0],1,1))
YValus = np.reshape(YValus,(YValus.shape[0],1,127))
'''Here's where the magic happens. It very much is magic to me, and a lot of this
im not super sure of what exactly is going on. You can play with most of the numbers and stuff
just to see what will happen, but for the most part its not going to make much sense'''
model = keras.Sequential()

model.add(keras.layers.Bidirectional(keras.layers.LSTM(512,activation = 'softmax',recurrent_activation = 'sigmoid',return_sequences=True, \

input_shape=(100,1))))
'''This is how many notes that the next note will be based off of. 
This makes actually a lot of difference. 
Try it for yourself between like 20 notes and 100.
'''

model.add(keras.layers.Dense(127))
model.add(keras.layers.Activation('softmax'))
optimizer = keras.optimizers.SGD(lr = 0.01)
model.compile(optimizer = 'rmsprop',loss = 'mean_squared_error')
#number of epochs here
Epo = 20
#start that shit and run right here
model.fit(XValus,YValus, epochs = Epo)
'''I should probably make a save statement RIGHT HERE.'''
anewsong = [XValus[0][0][0]]
for i in range(200):
    anewsong.append(chancer(model.predict(np.array([[[anewsong[-1]]]])),.4))
CWD = os.getcwd()
now = datetime.now() # current date and time
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
hours = now.strftime("%H")
mins = now.strftime("%M")
seconds = now.strftime("%S")
fullStr= year+month+day+hours+ mins +seconds
FileName = StripName+fullStr + "SuperSong.txt"
CreateText = open(FileName,'w')
for dude in anewsong:
    CreateText.write(str(dude)+'\n')
CreateText.write('\n')
CreateText.close()
StartP = CWD + "\\" + FileName
ExactPath = CWD + "\\NNMIDITESTS\\"+ FileName
shutil.move(StartP,ExactPath)
TTM.txttomidi(TTM.genMidiSamp(ExactPath,FileName[:-4]))
    
    


def GetNNData(direc, amount):
    '''I don't know why exactly I have this. I'd say the best bet is don't
    run it until i figure out why I made it. It's recursive, so that seems
    dangerous.'''
    listostuff = os.listdir(direc)
    inDirec = direc
    for i in range(amount): 
        randVal = random.randint(0, (len(listostuff)-1))
        currdir = inDirec + "\\" + listostuff[randVal]
        if(os.path.isdir(currdir)):
            outVal = GetNNData(currdir, 1)
            yield outVal
            continue
        yield listostuff[randVal]
        