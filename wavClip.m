function [outStream] = wavClip(inStream)
%Takes as input an array containing the converted audio file and clips the
%period before and after where the user is not speaking


% If input data is a column vector then transpose
if size(inStream, 2) == 1
    inStream = inStream';
end


maxval = max(inStream);
threshold = 0.2;
inFloor = zeros(size(inStream));
inFloor(inStream > threshold*maxval) = 1;

idxStart = find(inFloor, 1, 'first');
idxEnd = find(inFloor, 1, 'last');

if numel(idxStart) == 0
    idxStart = 1;
end
if numel(idxEnd) == 0
    idxEnd = numel(inStream);
end


idxStart = idxStart(1);
idxEnd = idxEnd(end);

outStream = inStream(idxStart:idxEnd);

end

