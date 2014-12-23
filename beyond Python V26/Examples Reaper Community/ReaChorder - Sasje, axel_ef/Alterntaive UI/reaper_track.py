# from reaper_python import *

debug = False

def msg(m):
    if debug:
        Reaper.ShowConsoleMsg(str(m) + "\n")

class Track:
    """ REAPER track class"""
    def __init__(self):
        msg("init Track class")

    def count(self):
        return Reaper.CountTracks(0)

    def insertAtIndex(self, index):
        """ Insert new track (at index) -> return track ID"""
        Reaper.InsertTrackAtIndex(0, index)
        Reaper.TrackList_AdjustWindows(False)  # Update track list
        return Reaper.GetTrack(0, index)

    def getIdAtIndex(self, index):
        """ Get track ID at index"""
        return Reaper.GetTrack(0, index)

    def setSelected(self, trackId):
        """ Set track selected (unselect other tracks)"""
##        Reaper.SetOnlyTrackSelected(trackId) # doesn't set "Last touched flag"?
        Reaper.Main_OnCommand(40297, 0)    # Unselect all tracks
        Reaper.SetMediaTrackInfo_Value(trackId, "I_SELECTED", True)

    def getSelected(self, index):
        """ Get selected track's ID at index"""
        return Reaper.GetSelectedTrack(0, index)

    def setName(self, trackId, name):
        """ Set track name"""
        name = str(name)
        return Reaper.GetSetMediaTrackInfo_String(trackId, "P_NAME", name, True)

class Item:
    """ REAPER item class"""
    def __init__(self):
        msg("init Item class")

    def getSelectedId(self, index):
        return Reaper.GetSelectedMediaItem(0, index)

    def getChunk(self, itemId):
        """ Get item chunk -> return chunk string"""
        return str(Reaper.GetSetItemState2(itemId, "", 1024**2*4, 1)[2])

    def getChunkInList(self, itemId):
        """ Get item chunk in list (keep the delimiter "\n")"""
        chunk = str(Reaper.GetSetItemState2(itemId, "", 1024**2*4, 1)[2])
        return chunk.splitlines(True)

    def insertMidiItem(self, trackIndex): #, position):
        """ Insert MIDI item to track at index x -> return item ID"""
##        position = float(position)
        track = Track()
        if track.count() == 0:
            track.insertAtIndex(0)
        trackId = track.getIdAtIndex(0)
        track.setSelected(trackId)
        cursorPos = float(Reaper.GetCursorPosition())

        try:
            Reaper.PreventUIRefresh(1)
##            Reaper.SetEditCurPos(position, 0, 0)
            insertNewMidiItem = 40214
            Reaper.Main_OnCommand(insertNewMidiItem, 0)
            Reaper.SetEditCurPos(cursorPos, 0, 0)
        finally:
            Reaper.PreventUIRefresh(-1)

        return self.getSelectedId(0)

    def setName(self, itemId, name):
        """ Set active take's name in item"""
        name = str(name)
        take = Reaper.GetActiveTake(itemId)
        return Reaper.GetSetMediaItemTakeInfo_String(take, "P_NAME", name, 1)

    def setLength(self, itemId, newLength):
        """ Set new item length (in seconds)"""
        newLength = float(newLength)
        Reaper.SetMediaItemInfo_Value(itemId, "D_LENGTH", newLength)

    def setMidiItemLength(self, itemId, lengthInMidiTicks, bps, quartNoteLength):
        """ Set new MIDI item length (in MIDI ticks)"""
        chunkL = []
        newLength = float(lengthInMidiTicks / quartNoteLength / bps)    # for 4/4
        self.setLength(itemId,newLength)
        chunk = str(Reaper.GetSetItemState2(itemId, "", 10 * 1024 ** 2, 1)[2])
        # Say(chunk)
        chunkL = chunk.splitlines(True)
        chunkL.reverse()

        for i, line in enumerate(chunkL):
            if line.startswith("E ") and line.split()[2] == "b0" and line.split()[3] == "7b":
                line = line.split()
                line[1] = int(lengthInMidiTicks)
                line = " ".join(str(x) for x in line)

                chunkL[i] = line + "\n"
                break

        chunkL.reverse()
        newChunk = "".join(str(c) for c in chunkL)
        # Say(newChunk)
        Reaper.GetSetItemState2(itemId, newChunk, len(newChunk), 1)
        Reaper.UpdateItemInProject(itemId)
