# Takes as input an array containing the converted audio file and clips the
# period before and after where the user is not speaking

import numpy as np
def wavClip(inStream):

    maxval = max(inStream)
    threshold = 0.2
    inFloor = np.zeros(len(inStream))
    inFloor[:] = [1 if ele > threshold*maxval else 0 for ele in inStream]
    idx = np.flatnonzero(inFloor)
    idxStart = idx[0]
    idxEnd = idx[-1]
    if len(idxStart) == 0:
        idxStart = 1
    if len(idxEnd) == 0:
        idxEnd = len(inStream)

    idxStart = idxStart[0]
    idxEnd = idxEnd[-1]
    outStream = inStream[idxStart:idxEnd]
    return outStream

