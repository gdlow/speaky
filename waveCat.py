import os
import numpy as np
import scipy.signal 
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import re

class TextToSpeech():
    def __init__(self):
        self.load_words('cmudict-0.7b.txt')

    def containsVowel(self,instr):
        #0 if no vowel, 1 if starts with vowel, 2 if ends with vowel, 3 if both
        #instr is a list
        vowels = 'aeiouAEIOU'
        if instr[0] in vowels and instr[-1] in vowels:
            result = 3
        elif instr[-1] in vowels:
            result = 2
        elif instr[0] in vowels:
            result = 1
        else:
            result = 0
        return result

    def vowelClip(self, phon, phonetic):
        cliplen = np.floor(len(phon)*0.2)
        result = self.containsVowel(phonetic)
        out = phon
        # if result == 2:
        #     out = phon[cliplen:]
        # elif result == 1:
        #     cliplenhalf = np.floor(cliplen*0.5)
        #     out = phon[:len(phon)-cliplenhalf]
        if result == 0:
            out = phon[0:int(len(phon)-cliplen)]

        return out

    def wavClip(self, inStream):
        maxval = max(inStream)
        threshold = 0.2
        inFloor = np.zeros(len(inStream))
        inFloor[:] = [1 if ele > threshold*maxval else 0 for ele in inStream]
        idx = np.flatnonzero(inFloor)
        idxStart = idx[0]
        idxEnd = idx[-1]
        if len(idxStart) == 0:
            idxStart = 1
        if len(idxEnd) == 0:
            idxEnd = len(inStream)

        idxStart = idxStart[0]
        idxEnd = idxEnd[-1]
        outStream = inStream[idxStart:idxEnd]
        return outStream


    def load_words(self, words_pron_dict:str):
        self.arpabet = {}
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ',2)
                    self.arpabet[key] = re.findall(r"[A-Z]+",val)
        return self.arpabet


    def get_pronunciation(self, str_input, filename):
        # Perform actual concatenation of input phonetics
        #arpabet = load_words('cmudict-0.7b.txt')
        list_pron = []
        completesentence = []
        print(str_input)
        print(str_input.split())
        for item in str_input.split():
            #if '?' or ',' or '.' or '!' in item[-1]:
            if item[-1] == '?' or item[-1] == '!' or item[-1] == '.' or item[-1] == ',':
                completesentence.append(item[:-1])
                completesentence.append(item[-1])
                completesentence.append('_') #input space
            elif item[-1] == ';' or item[-1] == ':' or item[-1] == '~':
                completesentence.append(item[:-1])
                completesentence.append('_')
            else:
                completesentence.append(item)
                completesentence.append('_')
        completesentence = completesentence[:-1]
        print(completesentence)
        # completesentence = re.findall(r"[\w']+",str_input)
        # #insert blank space between words in list
        # i=0
        # while i < len(completesentence):
        #     completesentence = completesentence[:i] + ["ZZZ"] + completesentence[i:]
        #     i += 2
        # print(completesentence[1:])      
        for word in completesentence:
            if word == '?':
                word = 'QNM'
            elif word == '!':
                word = 'EXM'
            elif word == ',':
                word = 'CMA'
            elif word == '.':
                word = 'FST'
            elif word == '_':
                word = 'SPC'
            if word.upper() in self.arpabet: #if the word is in the dictionary
                list_pron += self.arpabet[word.upper()]
        print(list_pron)
        testSentence = list_pron
        #testSentence = ['DH', 'AH', 'SPC', 'K', 'W', 'IH', 'K', 'SPC', 'B', 'R', 'AW', 'N', 'SPC', 'F', 'AA', 'K', 'S', 'CMA', 'SPC', 'JH', 'AH', 'M', 'P', 'T', 'SPC', 'OW', 'V', 'ER', 'SPC', 'DH', 'AH', 'SPC', 'W', 'AO', 'L', 'FST', 'SPC', 'S', 'AE', 'L', 'IY', 'SPC', 'W', 'AA', 'Z', 'SPC', 'N', 'AA', 'T', 'SPC', 'P', 'L', 'IY', 'Z', 'D', 'FST']
        testSentence = [item.lower() for item in testSentence]
        datastream = np.ndarray([0],dtype=np.float32);
        # joints = [] #For method 2
        joints = np.ndarray([0])
        Fs = 44100

        #parsing spaces and commas and other punctuations
        for i in range(len(testSentence)):
            item = testSentence[i]
            if item == 'spc':
                phon = np.zeros(int(Fs*0.1))
            elif item == 'cma':
                phon = np.zeros(int(Fs*0.3))
            elif item == 'fst':
                phon = np.zeros(int(Fs*0.4))
            elif item == 'exm':
                phon = np.zeros(int(Fs*0.4))
            elif item == 'qnm':
                phon = np.zeros(int(Fs*0.4))
            else:
                file = filename + testSentence[i] + ".wav"
                print (file)
                Fs, phon = scipy.io.wavfile.read(file)
                phon = self.vowelClip(phon, item)
            print (phon)
            datastream = np.append(datastream, phon);
            if i < len(testSentence):
                joints = np.append(joints, len(datastream))
        scipy.io.wavfile.write("phon.wav", Fs, phon)
        #Apply low pass filtering to smoothen the voice
        b,a = scipy.signal.butter(4,1500/(Fs/2))
        dataout = scipy.signal.lfilter(b,a,datastream)
        tmp = np.ndarray([0],dtype=np.float32)

        tmp = dataout
        tmp = tmp.astype(np.float32)

        #write audio to file

        tmp = tmp / np.max(tmp)
        scipy.io.wavfile.write('messages/datastream.wav', Fs, tmp)

if __name__ == '__main__':
    tts = TextToSpeech()
    tts.get_pronunciation('hey guys, i sound like you.','clippedAudio/ashley/')