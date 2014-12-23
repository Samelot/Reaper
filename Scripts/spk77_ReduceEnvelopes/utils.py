# in separate utils.py file

from reaper_python import *
from sws_python import *

def get_sel_env_chunk():
    fs = SNM_CreateFastString("")
    SNM_GetSetObjectState(RPR_GetSelectedTrackEnvelope(0), fs, 0, 0)
    chunk = SNM_GetFastString(fs)
    SNM_DeleteFastString(fs)
    return chunk

def set_sel_env_chunk(s):
    fs = SNM_CreateFastString(s)
    SNM_GetSetObjectState(RPR_GetSelectedTrackEnvelope(0), fs, 1, 0)
    SNM_DeleteFastString(fs)