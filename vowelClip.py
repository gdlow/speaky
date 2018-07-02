#function [out] = vowelClip(phon, str)
#vowelClip.py
import numpy as np 

def vowelClip(phon, string):
	cliplen = np.floor(len(phon)*0.25)
	result = containsVowel(string)
	out = phon
	if result == 2:
		out = phon[cliplen:]
	elif result == 1:
		cliplenhalf = np.floor(cliplen*0.5)
		out = phon[:len(phon)-cliplenhalf]
	elif result == 0:
		out = phon[:len(phon)-cliplen]

