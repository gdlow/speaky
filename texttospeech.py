#workflow changed to: 1. reads data 2. pulls together relevant phonetics 3. saves into messages folder.
import re
import wave
import time
# import matlab.engine
# eng = matlab.engine.start_matlab()

class TextToSpeech:
    
    CHUNK = 1024

    def __init__(self, words_pron_dict:str = 'cmudict-0.7b.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict:str):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ',2)
                    self._l[key] = re.findall(r"[A-Z]+",val)

    def get_pronunciation(self, str_input, filename):
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
            if word.upper() in self._l: #if the word is in the dictionary
                list_pron += self._l[word.upper()]
        print(list_pron)
        delay=0
        datastream = []
        for pron in list_pron:
            ###THIS HAS TO BE CHANGED###
            #_thread.start_new_thread( TextToSpeech._play_audio, (pron,delay,))
            #delay += 0.145

            #(workflow 3) stitch the wav files together
            w = wave.open(filename+"/"+pron.lower()+".wav",'rb')
            datastream.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        output = wave.open("messages/datastream.wav", 'wb')
        output.setparams(datastream[0][0])
        for i in range(len(datastream)):
            output.writeframes(datastream[i][1])
        output.close()
 
 

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        tts.get_pronunciation(input('Enter a word or phrase: '),"damon")

