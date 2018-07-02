function [out] = vowelClip(phon, str)

<<<<<<< HEAD
cliplen = floor(length(phon)*0.2);
=======
cliplen = floor(length(phon)*0.25);
>>>>>>> 8fbf7c8ed016d386dd6b9f3656973bc4cc85a5bb

result = containsVowel(str);

out = phon;
if result == 2
%     out = phon(cliplen:end);
elseif result == 1
%     out = phon(1:(end-cliplen*0.5));
elseif result == 0
    out = phon(1:(end-cliplen));
end    


end

