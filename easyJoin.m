function [dataout] = easyJoin(datastream, joints, Fs)

starts = [1]; ends = [];
interval = floor(Fs/10);
interval = min(interval, joints(1));
interval = min(interval, joints(end));
for i = 1:(length(joints)-1)
   before = datastream((joints(i)- interval + 1):joints(i)); 
   after = datastream((joints(i)+1):(joints(i)+interval));
   results = [];
   for j = 1:length(after)
     [c index] = min(abs(before-after(j)));  
     results = [results;[c, index+joints(i)-50, j+joints(i)]];
   end  
   best = find(results == min(results(:,1)),1);
   if numel(best) == 0
       disp(i);
   end
   ends = [ends, results(best,2)];
   starts = [starts, results(best,3)];
end
ends = [ends, length(datastream)];
dataout = [];
for i = 1:length(starts)
    dataout = [dataout, datastream(starts(i):ends(i))];
end

end

% starts = [1]; ends = [];
% interval = floor(Fs/10);
% interval = min(interval, joints(1));
% interval = min(interval, joints(end));
% for i = 1:(length(joints)-1)
%    before = datastream((joints(i)- interval + 1):joints(i)); 
%    after = datastream((joints(i)+1):(joints(i)+interval));
%    results = [];
%    for j = 1:length(after)
%      [c index] = min(abs(before-after(j)));  
%      results = [results;[c, index, j]];
%    end  
%    best = find(min(results(:,1),1));
%    if numel(best) == 0
%        disp(i);
%    end
%    ends = [ends, results(best,2)];
%    starts = [starts, results(best,3)];
% end
% ends = [ends, length(datastream)];
% dataout = [];
% for i = 1:length(starts)
%     dataout = [dataout, datastream(starts(i):ends(i))];
% end


% end

