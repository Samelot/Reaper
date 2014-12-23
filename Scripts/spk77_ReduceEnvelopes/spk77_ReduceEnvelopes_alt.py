from reaper_python import RPR_GetResourcePath as resPath
sys.path.append("{0}/Scripts".format(resPath()))

# Set selected envelope point(s) value(s)

from sws_python import *
from contextlib import contextmanager

import math
import shlex

@contextmanager
def undoable(message):
    RPR_Undo_BeginBlock2(0)
    try:
        yield
    finally:
        RPR_Undo_EndBlock2(0,message,-1)

def msg(m):
    RPR_ShowConsoleMsg(m)

def get_sel_env_chunk():
    fs = SNM_CreateFastString("")
    SNM_GetSetObjectState(RPR_GetSelectedTrackEnvelope(0), fs, 0, 0)
    chunk = SNM_GetFastString(fs)
    SNM_DeleteFastString(fs)
    if chunk:
        return chunk
    else:
        RPR_MB("No envelope selected", "", 0)
        chunk = ""
        return chunk

def set_sel_env_chunk(s):
    fs = SNM_CreateFastString(s)
    SNM_GetSetObjectState(RPR_GetSelectedTrackEnvelope(0), fs, 1, 0)
    SNM_DeleteFastString(fs)

def setSelectedEnvPointsVal():
    dialog = RPR_GetUserInputs("Set selected envelope points values", 1, "Set selected points to (dB):", "0", 100)
    if dialog[0] != 1:
        return
    try:
        newValueDB = float(dialog[4])
        if newValueDB > 6.02:   # upper limit
            newValueDB = 6.02
    except ValueError as e:
        msg(e)
        return

    chunk = get_sel_env_chunk()
    head = chunk[:chunk.find("PT") - 1]
    points = chunk[chunk.find("PT"):-3].split("\n")
    newValue = math.pow(10, newValueDB / 20)

    for i, point in enumerate(points):
        point = shlex.split(point)

        if len(point) == 6:
            point[2] = newValue  # change point

        new_point = "".join([str(i) + " " for i in point])
        points[i] = new_point + "\n"

    chunk = "%s\n%s>" % (head, "".join(points))
    set_sel_env_chunk(str(chunk))

with undoable('Set new values for selected envelope points'):
    setSelectedEnvPointsVal()