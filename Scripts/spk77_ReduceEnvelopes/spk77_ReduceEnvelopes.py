from reaper_python import RPR_GetResourcePath as resPath
sys.path.append("{0}/Scripts".format(resPath()))

from reaper_python import *
from contextlib import contextmanager

import math
import shlex
from utils import *

@contextmanager
def undoable(message):
    RPR_Undo_BeginBlock2(0)
    try:
        yield
    finally:
        RPR_Undo_EndBlock2(0,message,-1)

def adjustEnvelopePoints():
    chunk = get_sel_env_chunk()
    if not chunk:
        RPR_MB("No envelope selected", "", 0)
        return

    head = chunk[:chunk.find("PT") - 1]
    points = chunk[chunk.find("PT"):-3].split("\n")
    usr_input = RPR_GetUserInputs("Trim points gain", 1, "dB", "", 100)

    try:
        trim = math.pow(10, (float(usr_input[4]) / 20.0))
    except ValueError:
        return

    if usr_input[0] != 1:   # cancel pressed -> exit script
        return

    for i, point in enumerate(points):
        point = shlex.split(point)
        if len(point) == 6:
            point[2] = float(point[2]) * trim  # change point

        new_point = "".join([str(i) + " " for i in point])
        points[i] = new_point + "\n"

    chunk = "%s\n%s>" % (head, "".join(points))
    set_sel_env_chunk(str(chunk))

with undoable('Adjust envelope point(s) value'):
    adjustEnvelopePoints()