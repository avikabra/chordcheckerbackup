from scipy.io import wavfile
import math
# import matplotlib.pyplot as plt
import random
import numpy as np
#import sounddevice as sd
#from scipy.io.wavfile import write
import time
import os
from scipy.fftpack import fft

class ChordChecker:
    validNotes = {
        'lowE': 82,
        'lowF': 87,
        'lowG': 98,
        'lowA': 110,
        'lowB': 123,
        'lowC': 131,
        'lowD': 147,
        'middleE': 165,
        'middleF': 175,
        'middleG': 196,
        'middleG#': 208,
        'highA': 220,
        'highB': 247,
        'highC': 261,
        'highC#': 277,
        'highD': 293,
        'highE': 330,
        'highF': 349,
        'highF#': 370,
        'highG': 392
    }

    errorBounds = {
        'lowE': 2,
        'lowF': 2,
        'lowG': 3,
        'lowA': 3,
        'lowB': 3,
        'lowC': 4,
        'lowD': 4,
        'middleE': 4,
        'middleF': 5,
        'middleG': 5,
        'middleG#': 6,
        'highA': 6,
        'highB': 7,
        'highC': 7,
        'highC#': 7,
        'highD': 8,
        'highE': 9,
        'highF': 9,
        'highF#': 10,
        'highG': 11
    }

    noteLocations = {
        'lowF': '6th string open string',
        'lowF': '6th string 1rst fret',
        'lowG': '6th string 3rd fret',
        'lowA': '5th string open string',
        'lowB': '5th string 2nd fret',
        'lowC': '5th string 3rd fret',
        'lowD': '4th string open string',
        'middleE': '4th string 2nd fret',
        'middleF': '4th string 3rd fret',
        'middleG': '3rd string open string',
        'middleG#': '3rd string 1rst fret',
        'highA': '3rd string 2nd fret',
        'highB': '2nd string open string',
        'highC': '2nd string 1rst fret',
        'highC#': '2nd string 2nd fret',
        'highD': '2nd string 3rd fret',
        'highE': '1rst string open string',
        'highF': '1rst string 1rst fret',
        'highF#': '1rst string 2nd fret',
        'highG': '1th string 3rd fret'
    }

    chordBank = {
        'Am': ['highE', 'highC', 'highA', 'middleE', 'lowA'],
        'A': ['highE', 'highC#', 'highA', 'middleE', 'lowA'],
        'Em': ['highE', 'highB', 'middleG', 'middleE', 'lowB', 'lowE'],
        'E': ['highE', 'highB', 'middleG#', 'middleE', 'lowB', 'lowE'],
        'C': ['highE', 'highC', 'middleG', 'middleE', 'lowC'],
        'G': ['highG', 'highB', 'middleG', 'lowD', 'lowB', 'lowG'],
        'F': ['highF', 'highC', 'highA', 'middleF', 'lowC', 'lowF'],
        'D': ['highF#', 'highD', 'highA', 'lowD']
    }

    invalidChord = True

    def __init__(self, file, chord):
        """constructor"""
        self.file = file
        self.chord = chord

    def peakDetection(mX, t):
        thresh = np.where(np.greater(mX[1:-1], t), mX[1:-1], 0)
        next_minor = np.where(mX[1:-1]>mX[2:], mX[1:-1], 0)
        prev_minor = np.where(mX[1:-1]>mX[:-2], mX[1:-1], 0)
        ploc = thresh * next_minor * prev_minor
        ploc = ploc.nonzero()[0] + 1
        return ploc

    def processCheck(self,reccord_or_file):
        minBound = 40
        # print ('What is the filename? .mov to .wav?')
        # userFile = input()
        # invalidReq = False
        if (reccord_or_file == '1'):
            fs = 44100  # Sample rate
            seconds = 5  # Duration of recording
            # print('Recording starts in')
            for x in range(3):
                print(3-x)
                time.sleep(1) 
            print('recording...')
            # myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            # sd.wait()  # Wait until recording is finished
            # write('output.wav', fs, myrecording)
            # fs, audioData = wavfile.read('output.wav')
            # invalidReq = False
        elif (reccord_or_file == '2'):
            minBound = 8

        fs, audioData = wavfile.read(self.file)
        audioDataOld = audioData
        audioEx = audioData[0]
        if (isinstance(audioEx, np.ndarray)):
            audioData = []
            for x in range(len(audioDataOld)):
                audioData.append(audioDataOld[x][0])

        #prints sample rate, or the change in x for each second that passes in the recording
        print('sample rate: ' + str(fs))

        """ fig, (axs1, axs2) = plt.subplots(2)
        axs1.set_xlabel('time')
        axs1.set_ylabel('amplitude')
        axs2.set_xlabel('frequency')
        axs2.set_ylabel('amplitude') """

        xGraph = []
        for i in range(len(audioData)):
            xGraph.append(i)

        # axs1.plot(xGraph, audioData, label='Graph From File')

        #Creates new data set for the transform
        truncData = audioData

        #fourierTransform
        truncArray = np.array(truncData)
        mX = fft(truncArray)
        mXMod = abs(mX)/len(truncData)
        mXMod = mXMod[range(int(len(truncData)/int((fs/400))))]

        ploc = ChordChecker.peakDetection(mXMod, minBound)
        peaks = ploc * fs / len(truncData)
        print(peaks)

        # axs2.plot(frequencies, abs(fourierTransform))

        #prints the frequencies and checks if they are correct
        calcFreq = []

        for i in range(len(peaks)):
            calcFreq.append(int(peaks[i]))

        requiredFreq = []
        errorB = []
        boolElim = []
        for x in range(len(self.chordBank[self.chord])):
            indexF = self.chordBank[self.chord][x]
            requiredFreq.append(self.validNotes[indexF])
            errorB.append(self.errorBounds[indexF])
            boolElim.append(False)
        print('the required frequencies are ' + str(requiredFreq))

        removeL = []
        for g in range(len(requiredFreq)):
            for h in range(len(calcFreq)):
                if (requiredFreq[g] + errorB[g] >= calcFreq[h] and requiredFreq[g] - errorB[g] <= calcFreq[h]):
                    if (boolElim[g] == True):
                        removeL.append(calcFreq[h])
                    elif (boolElim[g] == False):
                        boolElim[g] = True

        for h in range(len(removeL)):
            calcFreq.remove(removeL[h])


        playedFreq = []
        for x in range(len(calcFreq)):
                for i in range(len(requiredFreq)):
                    if (calcFreq[x] >= requiredFreq[i] - errorB[i] and calcFreq[x] <= requiredFreq[i] + errorB[i]):
                        playedFreq.append([requiredFreq[i], calcFreq[x]])

        for p in range(len(playedFreq)):
            requiredFreq.remove(playedFreq[p][0])
            calcFreq.remove(playedFreq[p][1])

        reqPosition = []
        for i in range(len(requiredFreq)):
            for x, y in self.validNotes.items():
                if (y == requiredFreq[i]):
                    reqPosition.append(x)

        if (len(requiredFreq) == 0):
            print("You played the chord correctly!")
            return "You played the chord correctly!"
        else:
            rt=""
            print("\n The following notes need to be played or louder: " + str(reqPosition))
            rt+="The following notes need to be played or louder: " + str(reqPosition)+". "
            print("The locations of these notes are:")
            rt+="<br/> The locations of these notes are:\n"
            for h in range(len(reqPosition)):
                reqPosition[h] = self.noteLocations[reqPosition[h]]
                print(reqPosition[h])
                rt+=reqPosition[h]
                rt+=', '
            # print("their frequencies are " + str(requiredFreq))
            # print("these frequencies were heard but are not part of the chord: " + str(calcFreq))
            rt+="<br/> selected chord is is: " + str(self.chord)
            return rt    
        # plt.show()
        



    