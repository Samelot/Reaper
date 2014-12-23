from reaper_python import *
from contextlib import contextmanager

@contextmanager
def undoable(message):
    RPR_Undo_BeginBlock2(0)
    try:
        yield
    finally:
        RPR_Undo_EndBlock2(0,message,-1)

with undoable('Insert new track'):

    # int CountTracks(ReaProject* proj)
    #   count the number of tracks in the project (proj=0 for active project)

    lastTrackIndex = RPR_CountTracks(0)

    # void InsertTrackAtIndex(int idx, bool wantDefaults)
    #   inserts a track at idx,of course this will be clamped to 0..GetNumTracks().
    #   wantDefaults=TRUE for default envelopes/FX,otherwise no enabled fx/env

    RPR_InsertTrackAtIndex(lastTrackIndex, 1)

    # update view
    RPR_TrackList_AdjustWindows(False)
    RPR_UpdateArrange()