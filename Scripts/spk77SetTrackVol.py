# Normalize and reduce take volue

from reaper_python import *
from contextlib import contextmanager
import math

@contextmanager
def undoable(message):
    RPR_Undo_BeginBlock2(0)
    try:
        yield
    finally:
        RPR_Undo_EndBlock2(0,message,-1)

with undoable('Normalize and reduce take volue'):

    def msg(m):
        RPR_ShowConsoleMsg(m)

    def script():
        item = RPR_GetSelectedMediaItem(0, 0)
        take = RPR_GetTake(item, 0)

        old_sliderValue = math.pow(10, RPR_GetMediaItemTakeInfo_Value(take, "D_VOL") / 20.0)
        # old_vol = 20 * math.log10(RPR_GetMediaItemTakeInfo_Value(take, "D_VOL"))

        RPR_Main_OnCommandEx(40108, 0, 0)

        new_sliderValue = math.pow(10, RPR_GetMediaItemTakeInfo_Value(take, "D_VOL") / 20.0)        
        # new_vol = 20 * math.log10(RPR_GetMediaItemTakeInfo_Value(take, "D_VOL"))

        # sliderValue = math.pow(10, valueInDB / 20.0)

        vol = new_sliderValue - old_sliderValue
        RPR_SetMediaItemTakeInfo_Value(take, "D_VOL", vol)
        RPR_UpdateItemInProject(item)

        msg("volume math: "+ str(new_sliderValue) +" - "+ str(old_sliderValue) +" = "+ str(vol) +"\n")

    # do script
    script()