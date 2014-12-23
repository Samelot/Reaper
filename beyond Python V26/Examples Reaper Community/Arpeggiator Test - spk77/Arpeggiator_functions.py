##from sws_python import *
import beyond.Reaper
import itertools

from bisect import bisect_right, bisect_left
from random import randint
from contextlib import contextmanager

##noteList = ['0  C-1', '1  C#-1', '2  D-1', '3  D#-1', '4  E-1', '5  F-1', '6  F#-1', '7  G-1', '8  G#-1', '9  A-1', '10  A#-1', '11  B-1', '12  C0', '13  C#0', '14  D0', '15  D#0', '16  E0', '17  F0', '18  F#0', '19  G0', '20  G#0', '21  A0', '22  A#0', '23  B0', '24  C1', '25  C#1', '26  D1', '27  D#1', '28  E1', '29  F1', '30  F#1', '31  G1', '32  G#1', '33  A1', '34  A#1', '35  B1', '36  C2', '37  C#2', '38  D2', '39  D#2', '40  E2', '41  F2', '42  F#2', '43  G2', '44  G#2', '45  A2', '46  A#2', '47  B2', '48  C3', '49  C#3', '50  D3', '51  D#3', '52  E3', '53  F3', '54  F#3', '55  G3', '56  G#3', '57  A3', '58  A#3', '59  B3', '60  C4', '61  C#4', '62  D4', '63  D#4', '64  E4', '65  F4', '66  F#4', '67  G4', '68  G#4', '69  A4', '70  A#4', '71  B4', '72  C5', '73  C#5', '74  D5', '75  D#5', '76  E5', '77  F5', '78  F#5', '79  G5', '80  G#5', '81  A5', '82  A#5', '83  B5', '84  C6', '85  C#6', '86  D6', '87  D#6', '88  E6', '89  F6', '90  F#6', '91  G6', '92  G#6', '93  A6', '94  A#6', '95  B6', '96  C7', '97  C#7', '98  D7', '99  D#7', '100  E7', '101  F7', '102  F#7', '103  G7', '104  G#7', '105  A7', '106  A#7', '107  B7', '108  C8', '109  C#8', '110  D8', '111  D#8', '112  E8', '113  F8', '114  F#8', '115  G8', '116  G#8', '117  A8', '118  A#8', '119  B8', '120  C9', '121  C#9', '122  D9', '123  D#9', '124  E9', '125  F9', '126  F#9', '127  G9']
noteList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127']
##a = ([x.split()[0] for x in noteList])
##print(a)

def msg(m):
    with Reaper as r:
        r.ShowConsoleMsg(m)

@contextmanager
def undoable(message):
    with Reaper as r:
        r.Undo_BeginBlock2(0)
        try:
            yield
        finally:
    ##        msg(message)
            r.Undo_EndBlock2(0, message, -1)

def undo():
    with Reaper as r:
        r.Main_OnCommandEx(40029, 0, 0)   # undo 40029 - main section

def selectAllNotes(command_id=40003, islistviewcommand=0):
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

def unSelectAllNotes(command_id=40214, islistviewcommand=0):
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

def selAllNotesTselection(command_id=40746, islistviewcommand=0):
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

def deleteSelectedNotes(command_id=40002, islistviewcommand=0):
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(command_id, islistviewcommand)

def playStop():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40016, 0)

def cursorLeftbyGrid():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40047, 0)

def cursorRightbyGrid():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40048, 0)

def cursorLeftbyMeas():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40683, 0)

def cursorRightbyMeas():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40682, 0)

def cursorStartOfCurrMeas():
    with Reaper as r:
        r.Main_OnCommand(40838, 0)

def cursorStartOfNextMeas():
    with Reaper as r:
        r.Main_OnCommand(40837, 0)

def cursorToStartOfSel():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40872, 0)  # move cursor to start of selection in active MIDI item

def cursorToEndOfSel():
    with Reaper as r:
        r.MIDIEditor_LastFocused_OnCommand(40873, 0)  # move cursor to end of selection in active MIDI item

def cursorToStartOfItem():
    with Reaper as r:
##    with undoable("s"):
##    r.Undo_OnStateChange("s")
        r.Main_OnCommandEx(40289, 0, 0)   # main: unselect all
        actTake = getActTakeInEditor()
        item = r.GetMediaItemTake_Item(actTake)
        r.SetMediaItemInfo_Value(item, "B_UISEL", 1)
        r.Main_OnCommandEx(41173, 0, 0)   # move to start of selected item

def cursorToEndOfItem():
    with Reaper as r:
##    with undoable("e"):
##    r.Undo_OnStateChange("s")
        r.Main_OnCommandEx(40289, 0, 0)   # main: unselect all
        actTake = getActTakeInEditor()
        item = r.GetMediaItemTake_Item(actTake)
        r.SetMediaItemInfo_Value(item, "B_UISEL", 1)
        r.Main_OnCommandEx(41174, 0, 0)   # move to end of selected item

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

def countNotes(midiTake):
    """ Count of how many MIDI notes are in the MIDI take, returns notecount.
        int countNotes(RprMidiTake* midiTake)"""
    with Reaper as r:
        return r.FNG_CountMidiNotes(midiTake)


def getMidiNote(midiTake, index):
    """ Get a MIDI note from a MIDI take at specified index, returns a pointer of the current note.
        RprMidiNote* getMidiNote(RprMidiTake* midiTake, int index)"""
    with Reaper as r:
        return r.FNG_GetMidiNote(midiTake, index)


def getMidiNoteIntProperty(midiNote, prop):
    """Get MIDI note property, returns int value.
    int getMidiNoteIntProperty(RprMidiNote* midiNote, const char* property)"""
    with Reaper as r:
        return r.FNG_GetMidiNoteIntProperty(midiNote, prop)


def setMidiNoteIntProperty(midiNote, prop, value):
    """ Set MIDI note property - void setMidiNoteIntProperty(midiNote, constchar property, value)"""
    with Reaper as r:
        r.FNG_SetMidiNoteIntProperty(midiNote, prop, value)

def isInt(item):
    """ Check if value is integer - return 1 if true or 0 of not integer"""
    try:
        int(item)
        return True
    except ValueError:
        return False

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

def addPattern(patternL, root, channel, length, velocity):
    with Reaper as r:
        with undoable("Add pattern to MIDI editor"):
            r.MIDIEditor_LastFocused_OnCommand(40214, 0)  # unselect all

            midiTicksPerQuarterNote = int(r.SNM_GetIntConfigVar("miditicksperbeat", -1))
    ##        msg(midiTicksPerQuarterNote)
            if midiTicksPerQuarterNote == -1:
                msg("Couldn't get 'miditicksperbeat' from reaper.ini")
                return
    ##        SNM_SetIntConfigVar("miditicksperbeat", 960)
            midiTicksPerNote = midiTicksPerQuarterNote * 4
            length = int(midiTicksPerNote * length)
    ##        msg(length)
            octaveOffset = int(r.SNM_GetIntConfigVar("midioctoffs", -100) - 1)

    ##        r.MIDIEditor_LastFocused_OnCommand(40214, 0)  # unselect all
            r.MIDIEditor_LastFocused_OnCommand(40164, 0)  # insert note at current note

            midiTake = r.FNG_AllocMidiTake(r.MIDIEditor_GetTake(r.MIDIEditor_GetActive()))
            r.MIDIEditor_LastFocused_OnCommand(40755, 0) # set note pos to edit cursor

        ##    midiTake = FNG_AllocMidiTake(r.MIDIEditor_GetTake(r.MIDIEditor_GetActive()))
            notesCount = r.FNG_CountMidiNotes(midiTake)
            for i in range(notesCount):
                currNote = r.FNG_GetMidiNote(midiTake, i)
                currSel = r.FNG_GetMidiNoteIntProperty(currNote, "SELECTED")
                if currSel:
                    pos = int(r.FNG_GetMidiNoteIntProperty(currNote, "POSITION"))
    ##                velocity = int(FNG_GetMidiNoteIntProperty(currNote, "VELOCITY"))
                    r.FNG_SetMidiNoteIntProperty(currNote, "PITCH", root + patternL[0] - 12 * octaveOffset)
    ##                FNG_SetMidiNoteIntProperty(currNote, "VELOCITY", 96)
                    r.FNG_SetMidiNoteIntProperty(currNote, "CHANNEL", channel)
                    r.FNG_SetMidiNoteIntProperty(currNote, "LENGTH", length)
                    r.FNG_SetMidiNoteIntProperty(currNote, "VELOCITY", velocity)
                    break

            for i, note in enumerate(patternL[1:]):
                if root + note - 12 * octaveOffset > 127:
                    break
                else:
                    addNote(midiTake, channel, velocity, pos + length * (i + 1), root + note - 12 * octaveOffset, length, 1)

            r.FNG_FreeMidiTake(midiTake)
    ##        SNM_SetIntConfigVar("miditicksperbeat", midiTicksPerQuarterNote)
            cursorToEndOfSel()
    ##        item = r.GetMediaItemTake_Item(r.MIDIEditor_GetTake(r.MIDIEditor_GetActive()))
    ##        msg(item)
    ##        r.UpdateItemInProject(item)
    ##        r.UpdateArrange()
    ##        r.UpdateTimeline()

def addChordToEditCursor(pattern, rootNote, channel, length, velocity):
    with Reaper as r:
    ##    notePos()
    ##    track = r.GetTrack(0,0)
    ##    a = r.GetTrackMIDINoteName(0, 1, 0)
    ##    r.GetTrackMIDINoteName()
    ##    msg(r.GetToggleCommandState(40926))
    ##    msg(a)

        with undoable("Add chord"):
            r.Main_OnCommandEx(40289, 0, 0)   # Main:Unselect all

            octaveOffset = int(r.SNM_GetIntConfigVar("midioctoffs", -100) - 1)
            r.MIDIEditor_LastFocused_OnCommand(40214, 0)  # unselect all

            midiTicksPerQuarterNote = int(r.SNM_GetIntConfigVar("miditicksperbeat", -1))
            if midiTicksPerQuarterNote == -1:
                msg("Couldn't get 'miditicksperbeat' from reaper.ini")
                return

            midiTicksPerNote = midiTicksPerQuarterNote * 4
            length = int(midiTicksPerNote * length)

        ##    r.MIDIEditor_LastFocused_OnCommand(40214, 0)  # unselect all
            r.MIDIEditor_LastFocused_OnCommand(40164, 0)  # insert note at current note

            activeTake = r.MIDIEditor_GetTake(r.MIDIEditor_GetActive())
            midiTake = r.FNG_AllocMidiTake(activeTake)

    ##        r.Main_OnCommandEx(40289, 0, 0)   # Main: Unselect all

    ##        activeTake_item = r.GetMediaItemTake_Item(activeTake)
    ##        msg(activeTake_item)

    ##        r.SetMediaItemSelected(activeTake_item)
            r.MIDIEditor_LastFocused_OnCommand(40755, 0) # set note pos to edit cursor
            notesCount = r.FNG_CountMidiNotes(midiTake)
            for i in range(notesCount):
                currNote = r.FNG_GetMidiNote(midiTake, i)
                currSel = r.FNG_GetMidiNoteIntProperty(currNote, "SELECTED")
                if currSel:
                    pos = int(r.FNG_GetMidiNoteIntProperty(currNote, "POSITION"))
        ##            length = FNG_GetMidiNoteIntProperty(currNote, "LENGTH")
    ##                velocity = int(FNG_GetMidiNoteIntProperty(currNote, "VELOCITY"))
                    r.FNG_SetMidiNoteIntProperty(currNote, "PITCH", rootNote + pattern[0] - 12 * octaveOffset)
                    r.FNG_SetMidiNoteIntProperty(currNote, "CHANNEL", channel)
                    r.FNG_SetMidiNoteIntProperty(currNote, "LENGTH", length)
                    r.FNG_SetMidiNoteIntProperty(currNote, "VELOCITY", velocity)
                    pattern = pattern[1:]
                ##    msg(pattern)
                    for pitchChange in pattern:
    ##                    msg(pitchChange)
                        addNote(midiTake, channel, velocity, pos, rootNote + pitchChange - 12 * octaveOffset, length, 1)
                    r.FNG_FreeMidiTake(midiTake)
                    cursorToEndOfSel()
    ##                cursorPos = r.GetCursorPositionEx(0)
    ##                r.SetMediaItemLength(activeTake_item, cursorPos, 1)
    ##                r.Main_OnCommandEx(40612, 0, 0) # set item length to source media length
    ##                r.MIDIEditor_LastFocused_OnCommand(40639, 0)  # move edit cursor to end of selection
        ##            r.MIDIEditor_LastFocused_OnCommand(40752, 0)  # time sel to sel notes
    ##                break

def makeSelNoteIdList():
    """ Returns a list with noteIds (selected notes) and take's id."""
    noteIdList = []
    allocatedTake = allocateMIDITake(getActTakeInEditor())
    noteCount = countNotes(allocatedTake)
    for i in range(noteCount):
        if isNoteSelected(allocatedTake, i):
            noteIdList.append(getMidiNote(allocatedTake, i))
    return noteIdList, allocatedTake

def makeNoteIdList():
    """ Returns a list with noteIds (all notes) and take's id."""
    noteIdList = []
    allocatedTake = allocateMIDITake(getActTakeInEditor())
    noteCount = countNotes(allocatedTake)
    for i in range(noteCount):
        noteIdList.append(getMidiNote(allocatedTake, i))
    return noteIdList, allocatedTake

def isNoteSelected(allocatedTake, index):
    """ Returns 1 if selected, 0 if not selected"""
    isSelected = getMidiNoteIntProperty(getMidiNote(allocatedTake, index), "SELECTED")
    return isSelected


def applyPattern(pattern, rootNote, sel):
    """ Apply arpeggio-pattern to selected notes."""
    with Reaper as r:
        if sel == 1:
            message = "Apply arpeggio-pattern to selected notes"
        elif sel == 0:
            message = "Apply arpeggio-pattern to all notes"

        with undoable(message):
            r.Undo_OnStateChange2(0, "Apply arpeggio-pattern")

            a = 0
            newlist = []
            octaveOffset = int(r.SNM_GetIntConfigVar("midioctoffs", -100) - 1)
            if sel:
                noteIdList, allocatedTake = makeSelNoteIdList()
            else:
                noteIdList, allocatedTake = makeNoteIdList()
    ##        unSelectAllNotes()
            noteCount = countNotes(allocatedTake)
            div = int(noteCount / len(pattern)) + 1
            for i in range(div):
                newlist.append(pattern)
            merged = list(itertools.chain.from_iterable(newlist))
            for i in noteIdList:
                value = merged[a]
                setMidiNoteIntProperty(i, "PITCH", rootNote + value - 12 * octaveOffset)
                pos = r.FNG_GetMidiNoteIntProperty(i, "POSITION")
                length = r.FNG_GetMidiNoteIntProperty(i, "LENGTH")
                velocity = r.FNG_GetMidiNoteIntProperty(i, "VELOCITY")
    ##            addNote(allocatedTake, 1, velocity, pos, rootNote + merged[a+2] - 12 * octaveOffset, length, 1) ###################3
                addNote(allocatedTake, 1, velocity, pos, rootNote + value - 12 * octaveOffset, length, 1) ###################3
                a += 1
            r.FNG_FreeMidiTake(allocatedTake)

def applyToAllNotes(pattern, offS1, offS2):
    """ Apply selection pattern to all notes."""
    with Reaper as r:
        with undoable("Apply selection pattern to all notes"):
            offS1L = []
            offS2L = []
            if offS1 != 0:
                for i in range(offS1):
                    offS1L.insert(0, 0)

            if offS2 != 0:
                for i in range(offS2):
                    offS2L.append(0)

            r.Undo_OnStateChange2(0, "Apply selection pattern to all notes")
            a = 0
            newlist = []
            convertedList = []
            # sort pattern from lowest to highest
            pattern.sort()
            patternCopy = pattern[0:]
            for loopindex, n in enumerate(patternCopy):
                patternCopy[loopindex] = n - 1
                if patternCopy[loopindex] < 0:
                    msg("Error: indexing starts at 1")
                    return
            # get the highest value , and add 1 to it (it will be the convertedList's length)
            highest = max(patternCopy, key=int) + 1
            # if pattern is [1, 4, 8]...
            # convertedList would be [0, 0, 0, 0, 0, 0, 0, 0]
            for h in range(highest):
                convertedList.append(0)
            # replace zeros with "1" according to the pattern
            # if pattern is [1, 4, 8]...convertedList would be [1, 0, 0, 1, 0, 0, 0, 1]
            for v in patternCopy:
                convertedList[v] = 1
            noteIdList, allocatedTake = makeNoteIdList()
            noteCount = countNotes(allocatedTake)
            div = int(noteCount / len(convertedList)) + 1
            for x in range(div):
                newlist.append(offS1L + convertedList + offS2L)
            mergedList = list(itertools.chain.from_iterable(newlist))

    ##        if offS1L:
    ##            mergedList += offS1L
    ##
    ##        if offS2L:
    ##            mergedList += offS2L
    ##        msg(mergedList)

            for i in noteIdList:
                setMidiNoteIntProperty(i, "SELECTED", mergedList[a])
                a += 1
            freeMIDITake(allocatedTake)

def applyToSelNotes(pattern, offS1, offS2):
    """ Apply selection pattern to selected notes"""
    with Reaper as r:
        with undoable("Apply selection pattern to selected notes"):
            offS1L = []
            offS2L = []
            if offS1 != 0:
                for i in range(offS1):
                    offS1L.insert(0, 0)

            if offS2 != 0:
                for i in range(offS2):
                    offS2L.append(0)
            r.Undo_OnStateChange2(0, "Apply selection pattern to selected notes")
            a = 0
            newlist = []
            convertedList = []

            pattern.sort()
            patternCopy = pattern[0:]
            for loopindex, n in enumerate(patternCopy):
                patternCopy[loopindex] = n - 1
                if patternCopy[loopindex] < 0:
                    msg("Error: indexing starts at 1")
                    return
            highest = max(patternCopy, key=int) + 1
            for h in range(highest):
                convertedList.append(0)
            for v in patternCopy:
                convertedList[v] = 1
            noteIdList, allocatedTake = makeSelNoteIdList()
            noteCount = countNotes(allocatedTake)
            div = int(noteCount / len(convertedList)) + 1
            for x in range(div):
                newlist.append(offS1L + convertedList + offS2L)
            mergedList = list(itertools.chain.from_iterable(newlist))
            for i in noteIdList:
                setMidiNoteIntProperty(i, "SELECTED", mergedList[a])
                a += 1
            freeMIDITake(allocatedTake)

def flipSelNotes(listName):
    with Reaper as r:
        with undoable("Flip"):
            r.Undo_OnStateChange2(0, "Flip")
            l = []
            noteIdList, allocatedTake = makeSelNoteIdList()
            for currNote in noteIdList:
                l.append(r.FNG_GetMidiNoteIntProperty(currNote, listName))
            noteIdList.reverse()
            for i, id in enumerate(noteIdList):
                r.FNG_SetMidiNoteIntProperty(id, listName, l[i])
            freeMIDITake(allocatedTake)

def invertChord(direction):
    with Reaper as r:
        if direction == "Up":
            message = "Invert Up"
        else:
            message = "Invert Down"

        with undoable(message):
            r.Undo_OnStateChange2(0, "Invert")
            pitchList = []
            noteIdList, allocatedTake = makeSelNoteIdList()
            for currNote in noteIdList:
                pitch = r.FNG_GetMidiNoteIntProperty(currNote, "PITCH")
                pitchList.append(pitch)

            if direction == "Up":
                lowest = min(pitchList, key=int)
                for i, pitch in enumerate(pitchList):
                    if pitch == lowest and pitch + 12 < 127:
                        r.FNG_SetMidiNoteIntProperty(noteIdList[i], "PITCH", pitch + 12)

            if direction == "Down":
                highest = max(pitchList, key=int)
                for i, pitch in enumerate(pitchList):
                    if pitch == highest and pitch - 12 > 0:
                        r.FNG_SetMidiNoteIntProperty(noteIdList[i], "PITCH", pitch - 12)

            freeMIDITake(allocatedTake)

def selectRandomNotes():
    with Reaper as r:
        with undoable("Select random notes"):
            noteIdList, allocatedTake = makeNoteIdList()
            for i in noteIdList:
                rand = randint(0, 1)
                r.FNG_SetMidiNoteIntProperty(i, "SELECTED", rand)
            freeMIDITake(allocatedTake)

def setProperty(newValue, prop):
    with Reaper as r:
        propLowerC = str(prop.lower())
        with undoable("Set new " + propLowerC + " to selected notes"):
            r.Undo_OnStateChange2(0, "Set new length")

            noteIdlist, allocatedTake = makeSelNoteIdList()

            if prop == "LENGTH":
    ##            msg(newValue)
                midiTicksPerQuarterNote = int(r.SNM_GetIntConfigVar("miditicksperbeat", -1))
                if midiTicksPerQuarterNote == -1:
                    msg("Couldn't get 'miditicksperbeat' from reaper.ini")
                    return
                midiTicksPerNote = midiTicksPerQuarterNote * 4
                length = int(midiTicksPerNote * newValue)
                for i in noteIdlist:
                    r.FNG_SetMidiNoteIntProperty(i, "LENGTH", length)

            elif prop == "CHANNEL":
                for i in noteIdlist:
                    r.FNG_SetMidiNoteIntProperty(i, "CHANNEL", newValue)

            elif prop == "VELOCITY":
                for i in noteIdlist:
                    r.FNG_SetMidiNoteIntProperty(i, "VELOCITY", newValue)

            r.FNG_FreeMidiTake(allocatedTake)

    ##def notePos():
    ##    noteIdList, midiTake = makeSelNoteIdList()
    ##    for currNote in noteIdList:
    ##        pos = FNG_GetMidiNoteIntProperty(currNote, "POSITION")
    ##        length = FNG_GetMidiNoteIntProperty(currNote, "LENGTH")
    ####        FNG_SetMidiNoteIntProperty(currNote, "LENGTH", length * 2)
    ##        FNG_SetMidiNoteIntProperty(currNote, "POSITION", int(pos * 2))
    ##
    ##    FNG_FreeMidiTake(midiTake)
    ####    r.MIDIEditor_LastFocused_OnCommand(40181, 0)

def harmonizeSelected(root, hNote1, hNote2, fullScaleL, length, channel, velocity):
    with Reaper as r:
        with undoable("Harmonize (add notes)"):
            r.Undo_OnStateChange2(0, "Harmonize (add notes)")

            noteIdList, midiTake = makeSelNoteIdList()
            for currNote in noteIdList:
                pitch = r.FNG_GetMidiNoteIntProperty(currNote, "PITCH")
                pos = r.FNG_GetMidiNoteIntProperty(currNote, "POSITION")
                length = r.FNG_GetMidiNoteIntProperty(currNote, "LENGTH")

                if pitch in fullScaleL:
                    pitchPos = fullScaleL.index(pitch)
                    # prevent IndexError
                    if pitchPos + hNote1 > len(fullScaleL) - 1 or pitchPos + hNote2 > len(fullScaleL) - 1:
                        continue
                    # go to loop start if new note pos. (index) < 0
                    if pitchPos + hNote1 < 0 or pitchPos + hNote2 < 0:
                        continue

                    newNote1Pos = fullScaleL[pitchPos + hNote1]
                    newNote2Pos = fullScaleL[pitchPos + hNote2]

                    if hNote1 != 0 and 0 <= newNote1Pos <= 127:
                        addNote(midiTake, channel, velocity, pos, newNote1Pos, length, 1)
                    if hNote2 != 0 and 0 <= newNote2Pos <= 127:
                        addNote(midiTake, channel, velocity, pos, newNote2Pos, length, 1)

            r.FNG_FreeMidiTake(midiTake)

def transPoseScale(root, fullScaleL, direction):
    with Reaper as r:
        with undoable("TransPose to next/prev. note in scale"):
            r.Undo_OnStateChange2(0, "TransPose to next/prev. note in scale")

            selNoteIdL, midiTake = makeSelNoteIdList()

            for currNote in selNoteIdL:
                pitch = r.FNG_GetMidiNoteIntProperty(currNote, "PITCH")
                if pitch in fullScaleL:
                    pitchPos = fullScaleL.index(pitch)
                    # prevent IndexError
                    if direction == "UP" and pitchPos + 1 > len(fullScaleL) - 1:
                        continue
                    # don't try to transpose note if new index < 0 (in fullScaleL)
                    if direction == "DOWN" and pitchPos - 1 < 0:
                        continue

                    if direction == "UP":
                        r.FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos + 1])
                    elif direction == "DOWN":
                        r.FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos - 1])

                elif not pitch in fullScaleL:
                    if direction == "UP":
                        pitchPos = bisect_right(fullScaleL, pitch)
                        r.FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos])

                    if direction == "DOWN":
                        pitchPos = bisect_right(fullScaleL, pitch)
                        r.FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos - 1])

            r.FNG_FreeMidiTake(midiTake)

    ##def transPoseScaleKeepShape(root, fullScaleL, direction):
    ##    with undoable("TransPose to next/prev. note in scale"):
    ##        r.Undo_OnStateChange2(0, "TransPose to next/prev. note in scale")
    ##
    ##        selNoteIdL, midiTake = makeSelNoteIdList()
    ##
    ##        for i, currNote in enumerate(selNoteIdL):
    ##            pitch = FNG_GetMidiNoteIntProperty(currNote, "PITCH")
    ##            if pitch in fullScaleL:
    ##                if i == 0:
    ##                    firstNotePitch = pitch
    ##                pitchPos = fullScaleL.index(pitch)
    ##
    ##                # don't try to transpose note if new index < 0 (in fullScaleL)
    ##                if pitchPos - 1 < 0:
    ##                    continue
    ##
    ##                # prevent IndexError
    ##                if pitchPos + 1 > len(fullScaleL) - 1:
    ##                    continue
    ##                    FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos + 1])
    ##                elif direction == "DOWN":
    ##                    FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos - 1])
    ##
    ##            elif not pitch in fullScaleL:
    ##                if direction == "UP":
    ##                    pitchPos = bisect_right(fullScaleL, pitch)
    ##                    FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos])
    ##
    ##                if direction == "DOWN":
    ##                    pitchPos = bisect_right(fullScaleL, pitch)
    ##                    FNG_SetMidiNoteIntProperty(currNote, "PITCH", fullScaleL[pitchPos - 1])
    ##
    ##        FNG_FreeMidiTake(midiTake)