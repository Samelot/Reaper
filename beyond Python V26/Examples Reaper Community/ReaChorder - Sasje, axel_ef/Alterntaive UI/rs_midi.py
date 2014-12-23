# from reaper_python import *
# from sws_python import *

class MIDIEvent:
    def __init__(self):
        self.type
        self.channel
        self.value1
        self.value2


class RSMidi:
    """
    Requires SWS/S&M extensions.
    
    All static methods so we don't need to create an object to use them.
    just:  from rs_midi import *    and then:   RSMidi.cmdME(bling, blong)
    """ 
    
    @staticmethod
    def XcmdME(actME, cmd):
        Reaper.MIDIEditor_OnCommand(actME,cmd)
    
    
    @staticmethod
    def getActTakeInEditor():
        return Reaper.MIDIEditor_GetTake(Reaper.MIDIEditor_GetActive())
   

    @staticmethod
    def allocateMIDITake(midiTake):
        return Reaper.FNG_AllocMidiTake(midiTake)
    
    @staticmethod
    def freeMIDITake(midiTake):
        Reaper.FNG_FreeMidiTake(midiTake)
   
       
    @staticmethod
    def countNotes(midiTake):
        return Reaper.FNG_CountMidiNotes(midiTake)
    
    
    @staticmethod
    def getMidiNote(midiTake, index):
        return Reaper.FNG_GetMidiNote(midiTake, index)
    
    
    @staticmethod
    def getMidiNoteIntProperty(midiNote, prop):
        return Reaper.FNG_GetMidiNoteIntProperty(midiNote, prop)
    
    
    @staticmethod
    def setMidiNoteIntProperty(midiNote, prop, value):
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, prop, value)
    
    
    @staticmethod
    def selAllNotes(command_id=40003, islistviewcommand=0):
        Reaper.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)
    
    
    @staticmethod    
    def selAllNotesTselection(command_id=40746, islistviewcommand=0):
        Reaper.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)
    
    
    @staticmethod
    def deleteSelectedNotes(command_id=40002, islistviewcommand=0):       
        Reaper.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)
    
    
    @staticmethod
    def addNote(midiTake, ch, vel, pos, pitch, length, sel):
        midiNote = Reaper.FNG_AddMidiNote(midiTake)
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, "CHANNEL", ch)
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, "VELOCITY", vel)
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, "POSITION", pos)
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, "PITCH", pitch)
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, "LENGTH", length)
        Reaper.FNG_SetMidiNoteIntProperty(midiNote, "SELECTED", sel)