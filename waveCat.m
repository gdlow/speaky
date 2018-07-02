clear;
tic;
lookupfolder = 'clippedAudio';
destfolder = 'messages';
destfilename = 'matlabaudio';

% % Clean audio clips containing individual phonetics
<<<<<<< HEAD
f = dir('damon/*.wav');
for i = 1:length(f)
    currfile = f(i);
    [audioData, Fs] = audioread(sprintf('%s//%s',currfile.folder,currfile.name));
    clipped = wavClip(audioData);
    audiowrite(sprintf('%s//%s',lookupfolder, currfile.name), clipped, Fs);
end
=======
% f = dir('ger_eg/*.wav');
% for i = 1:length(f)
%     currfile = f(i);
%     [audioData, Fs] = audioread(sprintf('%s//%s',currfile.folder,currfile.name));
%     clipped = wavClip(audioData);
%     audiowrite(sprintf('%s//%s',lookupfolder, currfile.name), clipped, Fs);
% end
>>>>>>> 8fbf7c8ed016d386dd6b9f3656973bc4cc85a5bb

% Perform actual concatenation of input phonetics
% testSentence = {'HH', 'AH', 'L', 'OW', 'AY', 'AE', 'M', 'AH', 'R', 'OW', 'B', 'AA', 'T', 'AY', 'L', 'AY', 'K', 'T', 'UW', 'IY', 'T', 'AE', 'P', 'AH', 'L', 'Z'};
testSentence = {'HH', 'AH', 'L', 'OW',...
    ',',...
    'AY',...
    ' ',...
    'AE', 'M',...
    ' ',...
    'AH',...
    ' ',...
    'R', 'OW', 'B', 'AA', 'T',...
    '.',...
    'AY',...
    ' ',...
    'L', 'AY', 'K',...
    ' ',...
    'T', 'UW',...
    ' ',...
    'IY', 'T',...
    ' ',...
    'AE', 'P', 'AH', 'L', 'Z'};
<<<<<<< HEAD
testSentence = {'DH', 'EH', 'R', 'Z', 'ZZZ', 'AH', 'ZZZ', 'HH', 'AH', 'N', 'D', 'R', 'AH', 'D', 'ZZZ', 'AH', 'N', 'D', 'ZZZ', 'F', 'AO', 'R', 'ZZZ', 'D', 'EY', 'Z', 'ZZZ', 'AH', 'V', 'ZZZ', 'S', 'AH', 'M', 'ER', 'ZZZ', 'V', 'EY', 'K', 'EY', 'SH', 'AH', 'N', 'ZZZ', 'DH', 'EH', 'N', 'ZZZ', 'S', 'K', 'UW', 'L', 'ZZZ', 'K', 'AH', 'M', 'Z', 'ZZZ', 'AH', 'L', 'AO', 'NG', 'ZZZ', 'JH', 'AH', 'S', 'T', 'ZZZ', 'T', 'UW', 'ZZZ', 'EH', 'N', 'D', 'ZZZ', 'IH', 'T'};

testSentence = lower(testSentence);

datastream = [];
=======
% testSentence = {'DH', 'EH', 'R', 'Z', 'ZZZ', 'AH', 'ZZZ', 'HH', 'AH', 'N', 'D', 'R', 'AH', 'D', 'ZZZ', 'AH', 'N', 'D', 'ZZZ', 'F', 'AO', 'R', 'ZZZ', 'D', 'EY', 'Z', 'ZZZ', 'AH', 'V', 'ZZZ', 'S', 'AH', 'M', 'ER', 'ZZZ', 'V', 'EY', 'K', 'EY', 'SH', 'AH', 'N', 'ZZZ', 'DH', 'EH', 'N', 'ZZZ', 'S', 'K', 'UW', 'L', 'ZZZ', 'K', 'AH', 'M', 'Z', 'ZZZ', 'AH', 'L', 'AO', 'NG', 'ZZZ', 'JH', 'AH', 'S', 'T', 'ZZZ', 'T', 'UW', 'ZZZ', 'EH', 'N', 'D', 'ZZZ', 'IH', 'T'};

testSentence = lower(testSentence);

datastream = []; 
>>>>>>> 8fbf7c8ed016d386dd6b9f3656973bc4cc85a5bb
joints = []; % For method 2
Fs = 44100;
for i = 1:length(testSentence)
    if contains(testSentence{i},' ') || contains(testSentence{i},'zzz')
        phon = zeros(Fs*0.1, 1);
    elseif testSentence{i} == ','
        phon = zeros(Fs*0.2, 1);
    elseif testSentence{i} == '.'
        phon = zeros(Fs*0.3, 1);
    else
<<<<<<< HEAD
        [phon, Fs] = audioread(sprintf('%s//%s.wav',lookupfolder,testSentence{i}));
%         [phon, Fs] = audioread(sprintf('%s//%s.wav',lookupfolder,testSentence{i}), 'native');
%         phon = double(phon);
=======
        [phon, Fs] = audioread(sprintf('%s//%s.wav',lookupfolder,testSentence{i}), 'native');
>>>>>>> 8fbf7c8ed016d386dd6b9f3656973bc4cc85a5bb
        phon = vowelClip(phon, testSentence{i});
    end
    datastream = [datastream, phon']; 
    if i < length(testSentence)
        joints = [joints, length(datastream)];
    end
end
%   Apply some filtering to smoothen the voice   %
% #############   TRY THINGS HERE   ############################
dataout = datastream;
% % % %   Method 1: simple moving average filter
% % % N = 10;
% % % dataout = filter(ones(1,N)./N,1,datastream);

%   Method 2: Minimize joining difference
<<<<<<< HEAD
% dataout = easyJoin(datastream, joints, Fs);

%   Method 4: easyJoin V2 - interpolation
dataout = datastream;
ninterp = Fs*0.1;
if joints(1) < ninterp
    ninterp = joints(1)-2;
end
if length(dataout)-joints(end) < ninterp
    ninterp = length(dataout)-joints(end)-2;
end
for i = 1:length(joints)
    before = dataout((joints(i)-ninterp-1):(joints(i)-1));
    after = dataout((joints(i)):(joints(i)+ninterp));
    combined = easyInterp(before,after,ninterp-2);
    dataout((joints(i)-ninterp-1):(joints(i)+ninterp)) = combined(1:(end-1));
end
=======
dataout = easyJoin(datastream, joints, Fs);
>>>>>>> 8fbf7c8ed016d386dd6b9f3656973bc4cc85a5bb

%   Method 3: Low Pass Filter to remove blips
[b,a] = butter(4, 1500/(Fs/2));
dataout = filter(b,a,dataout);

audiowrite(sprintf('%s//%s.wav',destfolder,destfilename), dataout, Fs);
toc;
sound(audioread(sprintf('%s//%s.wav',destfolder,destfilename)), Fs);







