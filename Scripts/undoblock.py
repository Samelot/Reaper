from reaper_python import *
from contextlib import contextmanager

@contextmanager
def undoable(message):
    RPR_Undo_BeginBlock2(0)
    try:
        yield
    finally:
        RPR_Undo_EndBlock2(0,message,-1)


with undoable('Split item(s)'):
    SelectItemUnderCursor = 40528
    DeselectItems = 40289
    MoveCursor = 40513
    SplitItems = RPR_NamedCommandLookup('_SWS_AWSPLITXFADELEFT')
    SelectPreviousItem = RPR_NamedCommandLookup('_SWS_SELPREVITEM2')
    CrossfadeToTimeSel = 40916


    selItems = RPR_CountSelectedMediaItems(0)
    timeSel = RPR_GetSet_LoopTimeRange2(0, 0, 0, 0, 0, 0)[3] != RPR_GetSet_LoopTimeRange2(0, 0, 0, 0, 0, 0)[4]

    RPR_Main_OnCommand(MoveCursor, 0)

    if (selItems==0):
      RPR_Main_OnCommand(SelectItemUnderCursor, 0)
      RPR_Main_OnCommand(SplitItems, 0)
      if (timeSel!=0):
        RPR_Main_OnCommand(SelectPreviousItem, 0)
        RPR_Main_OnCommand(CrossfadeToTimeSel, 0)
      RPR_Main_OnCommand(DeselectItems, 0)

    if (selItems!=0):
      RPR_Main_OnCommand(SplitItems, 0)
      if (timeSel!=0):
        RPR_Main_OnCommand(SelectPreviousItem, 0)
        RPR_Main_OnCommand(CrossfadeToTimeSel, 0)