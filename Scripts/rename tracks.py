# Rename tracks to take source filename (without file extension)

# take = first item's active take



from reaper_python import *

from contextlib import contextmanager

import os



@contextmanager

def undoable(message):

    RPR_Undo_BeginBlock2(0)

    try:

        yield

    finally:

        RPR_Undo_EndBlock2(0, message, -1)



with undoable("Rename tracks to source file name"):



    def msg(m):

        RPR_ShowConsoleMsg(m)



    def renameToSourceFileName():

        trackCount = RPR_CountSelectedTracks(0)



        if trackCount < 1:

            msg("")

            msg("Select tracks first")

            return



        for i in range(trackCount):

            trackId = RPR_GetSelectedTrack(0, i)

            itemCount = RPR_CountTrackMediaItems(trackId)

            if itemCount == 0:

                continue



            itemId = RPR_GetTrackMediaItem(trackId, 0)   # get id from first item in track

            takeId = RPR_GetActiveTake(itemId)  # get id from active take in item

            takeSource = RPR_GetMediaItemTake_Source(takeId)

            fullPath = str(RPR_GetMediaSourceFileName(takeSource, "", 512)[1])



            if fullPath == "":  # ignore in-project MIDI

                continue



            fileName = os.path.split(fullPath)[-1][:-4]   # get filename and remove file extension



            RPR_GetSetMediaTrackInfo_String(trackId, "P_NAME", fileName, 1)



    renameToSourceFileName()