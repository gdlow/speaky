#function vowel = containsvowel
#containsvowel.m

def containsVowel(instr):
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
