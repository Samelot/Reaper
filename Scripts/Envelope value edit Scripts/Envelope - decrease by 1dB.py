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

with undoable('Decrease selected envelope points by 1dB'):

    chunk = get_sel_env_chunk()
    head = chunk[:chunk.find("PT") - 1]
    points = chunk[chunk.find("PT"):-3].split("\n")
    trim = math.pow(10, -1 / 20.0)

    for i, point in enumerate(points):
        point = shlex.split(point)
        try:
            if int(point[5]):
                point[2] = float(point[2]) * trim  # change point
        except:
            pass

        new_point = "".join([str(i) + " " for i in point])
        points[i] = new_point + "\n"

    chunk = "%s\n%s>" % (head, "".join(points))
    set_sel_env_chunk(str(chunk))