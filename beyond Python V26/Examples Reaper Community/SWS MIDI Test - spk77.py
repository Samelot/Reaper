import beyond.Reaper
import beyond.Screen
##from sws_python import *

def msg(m):
    with Reaper as r:
        r.ShowConsoleMsg(m)

def getActTakeInEditor():
    """Returns the pointer of the currently active take in the midieditor."""
    with Reaper as r:
        return r.MIDIEditor_GetTake(r.MIDIEditor_GetActive())

def allocateMIDITake(midiTake):
    """ Allocate a RprMidiTake from a take pointer. Returns a NULL pointer if the take is not an in-project MIDI take.
        RprMidiTake* allocateMIDITake(MediaItem_Take* take)"""
    with Reaper as r:
        return r.FNG_AllocMidiTake(midiTake)

def freeMIDITake(allocatedTake):
    """ Commit changes to MIDI take and free allocated memory.
        void freeMIDITake(RprMidiTake* midiTake)"""
    with Reaper as r:
        r.FNG_FreeMidiTake(allocatedTake)

def selectAllNotes(command_id=40003, islistviewcommand=0):
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

def deleteSelectedNotes(command_id=40002, islistviewcommand=0):
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

def addNote(midiTake, ch, vel, pos, pitch, length, sel):
    with Reaper as r:
        midiNote = r.FNG_AddMidiNote(midiTake)
        r.FNG_SetMidiNoteIntProperty(midiNote, "CHANNEL", ch)
        r.FNG_SetMidiNoteIntProperty(midiNote, "VELOCITY", vel)
        r.FNG_SetMidiNoteIntProperty(midiNote, "POSITION", pos)
        r.FNG_SetMidiNoteIntProperty(midiNote, "PITCH", pitch)
        r.FNG_SetMidiNoteIntProperty(midiNote, "LENGTH", length)
        r.FNG_SetMidiNoteIntProperty(midiNote, "SELECTED", sel)
        return midiNote

@ProgramStart
def Main():
    Reaper.OnConnectExecute = "from sws_python import *"
    with Reaper as r:
        selectAllNotes()
        deleteSelectedNotes()

        midiTicksPerQuarterNote = int(r.SNM_GetIntConfigVar("miditicksperbeat", -1))
        position = 0
        melody = [48, 52, 55, 60, 64, 67]
        melody2 = [43, 48, 52, 55, 60, 64]
        melody3 = [52, 55, 60, 64, 67, 72]
        take = r.MIDIEditor_GetTake(r.MIDIEditor_GetActive())
        allocated = allocateMIDITake(take)
        for i, note in enumerate(melody):
            addNote(allocated, 1, 72, position, note, int(midiTicksPerQuarterNote * 4 / 6), 1)
            addNote(allocated, 1, 72, position, melody2[i], int(midiTicksPerQuarterNote * 4 / 6), 1)
            addNote(allocated, 1, 72, position, melody3[i], int(midiTicksPerQuarterNote * 4 / 6), 1)
            position += int(midiTicksPerQuarterNote * 4 / 6)

        addNote(allocated, 1, 72, position, 60, int(midiTicksPerQuarterNote * 4), 1)
        addNote(allocated, 1, 72, position, 55, int(midiTicksPerQuarterNote * 4), 1)
        addNote(allocated, 1, 72, position, 48, int(midiTicksPerQuarterNote * 4), 1)
        addNote(allocated, 1, 72, position, 76, int(midiTicksPerQuarterNote * 4), 1)

        freeMIDITake(allocated)