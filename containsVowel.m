function [result] = containsVowel(instr)
% 0 if no vowel, 1 if starts with vowel, 2 if ends with vowel, 3 if both
vowels = 'aeiouAEIOU';
if contains(vowels, instr(1)) && contains(vowels, instr(end))
    result = 3;
elseif contains(vowels, instr(end))
    result = 2;
elseif contains(vowels, instr(1))    
    result = 1;
else 
    result = 0;
end    

end

