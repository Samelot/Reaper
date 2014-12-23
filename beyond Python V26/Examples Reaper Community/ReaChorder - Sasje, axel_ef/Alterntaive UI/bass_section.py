# from reaper_python import *
from rs_midi import RSMidi
import reaChord_data
import tkinter
from tkinter import ttk
from rs_statemanager import RSStateManager



class BassSection(RSStateManager):
    '''
    Root note per chord, transposed down
    '''

    #rc = reaChord_functions.RC() # comment out - for autocomplete


    def __init__(self, parent, rc):
        '''

        '''
        self.settings = {
            "draw": 1, "channel": 3, "velocity": 96, "highlight": 1, "invert_above": 6
        }
        self.stateManager_Start("BassSection", self.settings) 
        self.msg("Bass __init__  Enter")
        #self.sta
        self.parent = parent
        self.rc = rc
        self.init_widgets()
        self.msg("Bass __init__  Exit")



    def draw(self, midiTake, song, sectionLength):
        #song dictionary contains full Structure and chords for the sections
        # ie Verse and Chorus at the moment.
        if not(self.drawOrNot.get()): return
        currentPos = 0

        for i, sect in enumerate(song["Structure"]):
            chords = song[str(sect)]
            chordLength = sectionLength / len(chords)
            for chord in chords:
                self.drawBass(midiTake, chord, currentPos, chordLength)
                currentPos += chordLength
        return currentPos



    def drawBass(self,midiTake, chord, currentPos, chordLength):
        self.msg('drawBass - Enter')
        velocity = self.velocity.get()
        selectNote = self.highlight.get()
        channel = self.channel.get()
        drop = 24
        RSMidi.addNote(midiTake, channel, int(velocity), int(currentPos),\
                            int(self.rc.ChordDict[chord][0])-drop, int(chordLength), selectNote)

        self.msg('drawBass - Exit')
        return currentPos



    def init_widgets(self):
        # Widget Initialization

        self._label_1 = tkinter.Label(self.parent,
            text = "Draw:",bg="#D9D9D9",
        )
        self._label_2 = tkinter.Label(self.parent,
            text = "Highlight:",bg="#D9D9D9",
        )
        self._label_3 = tkinter.Label(self.parent,
            text = "Channel:",bg="#D9D9D9",
        )
        self._label_4 = tkinter.Label(self.parent,
            text = "Velocity:",bg="#D9D9D9",
        )

        
        self.drawOrNot = self.newControlIntVar("draw", 1)
        self.cDrawOrNot = tkinter.Checkbutton(self.parent, variable=self.drawOrNot,bg="#D9D9D9")
       
        self.highlight = self.newControlIntVar("highlight", 0)
        self.cHighlight = tkinter.Checkbutton(self.parent, variable=self.highlight,bg="#D9D9D9")
        
        self.channel = self.newControlIntVar("channel", 3)
        self.sChannel = tkinter.Scale(self.parent, from_=1, to=16, resolution=1, showvalue=0, orient="horizontal",\
                                      variable=self.channel)
        self.scaleTxt1 = ttk.Label(self.parent, textvariable=self.channel)
        
        self.velocity = self.newControlIntVar("velocity", 96)
        self.sVelocity = tkinter.Scale(self.parent, from_=1, to=127, resolution=1, showvalue=0, orient="horizontal",\
                                       variable=self.velocity)
        self.scaleTxt2 = ttk.Label(self.parent, textvariable=self.velocity)
        
        # Geometry Management

        self._label_1.grid(
            in_    = self.parent,
            column = 1,
            row    = 1,
            columnspan = 1,
            ipadx = 10,
            ipady = 5,
            padx = 0,
            pady = 5,
            rowspan = 1,
            sticky = "w"
        )
        self._label_2.grid(
            in_    = self.parent,
            column = 1,
            row    = 2,
            columnspan = 1,
            ipadx = 10,
            ipady = 5,
            padx = 0,
            pady = 5,
            rowspan = 1,
            sticky = "w"
        )
        self._label_3.grid(
            in_    = self.parent,
            column = 1,
            row    = 3,
            columnspan = 1,
            ipadx = 10,
            ipady = 5,
            padx = 0,
            pady = 5,
            rowspan = 1,
            sticky = "w"
        )
        self._label_4.grid(
            in_    = self.parent,
            column = 1,
            row    = 4,
            columnspan = 1,
            ipadx = 10,
            ipady = 5,
            padx = 0,
            pady = 5,
            rowspan = 1,
            sticky = "w"
        )

        self.scaleTxt1.grid(
            in_    = self.parent,
            column = 2,
            row    = 3,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 2,
            pady = 0,
            rowspan = 1,
            sticky = "e"
        )
        self.scaleTxt2.grid(
            in_    = self.parent,
            column = 2,
            row    = 4,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 2,
            pady = 0,
            rowspan = 1,
            sticky = "e"
        )

        self.cDrawOrNot.grid(
            in_    = self.parent,
            column = 2,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )
        self.cHighlight.grid(
            in_    = self.parent,
            column = 2,
            row    = 2,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )
        self.sVelocity.grid(
            in_    = self.parent,
            column = 2,
            row    = 4,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )

        self.sChannel.grid(
            in_    = self.parent,
            column = 2,
            row    = 3,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )
        self.parent.grid_rowconfigure(1, weight = 0, minsize = 22, pad = 0)
        self.parent.grid_rowconfigure(2, weight = 0, minsize = 22, pad = 0)
        self.parent.grid_rowconfigure(3, weight = 0, minsize = 22, pad = 0)
        self.parent.grid_rowconfigure(4, weight = 0, minsize = 22, pad = 0)
        self.parent.grid_rowconfigure(5, weight = 0, minsize = 22, pad = 0)
        self.parent.grid_rowconfigure(6, weight = 0, minsize = 22, pad = 0)
        self.parent.grid_columnconfigure(1, weight = 0, minsize = 80, pad = 0)
        self.parent.grid_columnconfigure(2, weight = 0, minsize = 135, pad = 0)




    def msg(self, m):
        if (reaChord_data.debug):
            Reaper.ShowConsoleMsg(str(m)+'\n')