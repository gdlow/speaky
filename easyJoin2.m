function [dataout] = easyJoin2(datastream, joints, Fs)

starts = [1]; ends = [];
interval = floor(Fs/10);
interval = min(interval, joints(1));
interval = min(interval, joints(end));

dataout = [];

for i = 1:(length(joints)-1)
   before = datastream((joints(i)- interval + 1):joints(i)); 
   after = datastream((joints(i)+1):(joints(i)+interval)); 
   combined = easyInterp(before, after, floor(interval/100000));
   dataout = [dataout, combined];
end

end
