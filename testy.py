#to test wave on converted file from cloudconvert.
import re
import wave
import os
# datastream = []
# for i in range(2):
#     w = wave.open('testy'+".wav",'rb')
#     datastream.append( [w.getparams(), w.readframes(w.getnframes())] )
#     w.close()
# output = wave.open("datastream.wav", 'wb')
# output.setparams(datastream[0][0])
# for i in range(len(datastream)):
#     output.writeframes(datastream[i][1])
# output.close()

# string = 'aa.wav'

# print(string[:-4])

# wavdict = {}
# for i,item in enumerate(sorted(os.listdir("damon"))):
#     wavdict[i] = item[:-4] #just take the name without .wav
# print(wavdict)
# print(wavdict[len([1,2])])

sentence = ['i','am','groot']

i=0
while i < len(sentence):
	sentence = sentence[:i] + ["_"] + sentence[i:]
	i += 2
print(sentence)
example = 'The quick brown fox jumped over the fence . The sly cat didn\'t notice .'
print(example.split())

string = 'i am group'
print(string[-1])
import numpy as np
print(np.floor(3.14))

testSentence = ['HH', 'AH', 'L', 'OW', 'AY', 'AE', 'M', 'AH', 'R', 'OW', 'B', 'AA', 'T', 'AY', 'L', 'AY', 'K', 'T', 'UW', 'IY', 'T', 'AE', 'P', 'AH', 'L', 'Z']
testSentence = [item.lower() for item in testSentence]
print(testSentence)

zeroarray = np.zeros(int(44100*0.1))
print(zeroarray)
print(max(testSentence))
instream = [2,3,4,5,6,78,2,3,2,4,5,2,41,23,52,352,1,0]
zeroarray = np.zeros(len(instream))
zeroarray = [1 if ele > 3 else 0 for ele in instream]
print(zeroarray)

instream=np.array(instream)
print(instream)

print(string[-1])