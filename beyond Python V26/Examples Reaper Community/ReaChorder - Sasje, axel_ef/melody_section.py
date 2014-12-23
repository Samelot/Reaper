# from reaper_python import *
from rs_midi import RSMidi
from random import randint
import reaChord_data
import tkinter
from tkinter import ttk
from rs_statemanager import RSStateManager


class MelodySection(RSStateManager):    ## <<<< we are now inheriting from RSStateManager
    '''
    Melody madness
    '''

    #rc = reaChord_functions.RC() # comment out - for autocomplete

    def __init__(self, parent, rc):

        self.settings = {
            "draw": 1, "channel": 2, "velocity": 96, "highlight": 1, "extranoteprobability" : 50
        }
        self.msg("Chords __init__  Enter")
        
        #      V           V          V            V 
        #since we are inheriting from RSStateManager, there is another instance of that
        #class combined with MelodySection.  So we set the instance variables with
        #what we need for this section....  (now see init_widgets)
        self.stateManager_Start("MelodySection", self.settings) 
        
        self.parent = parent
        self.rc = rc
        self.init_widgets()
        self.msg("Chords __init__  Exit")
        


    def draw(self, midiTake, song, sectionLength):
        #song dictionary contains full Structure and chords for the sections
        # ie Verse and Chorus at the moment.
        if not(self.drawOrNot.get()): return
        currentPos = 0

        # melodyType = self.MelodyTypeSel.current()

        # iterate through the song structure, "VVCCVCVCVV"....
        for i, sect in enumerate(song["Structure"]):
            #... and get the list of chords for the verse, or chorus
            chords = song[str(sect)]
            chordLength = sectionLength / len(chords)
            for chord in chords:
                #send the chord NAME to drawMelody
                self.drawMelody(midiTake, chord, currentPos, chordLength)
                currentPos += chordLength
        return currentPos



    def drawMelody(self,midiTake, chord, currentPos, chordLength):
        self.msg('drawMelody - Enter')
        harmony1 = True # if True, add "harmony1"
        harmony2 = False # if True, add "harmony2"
        randNote = randint(2, 3)
        randPos = [0,480,960]

        randLength = [0.5, 1, 2]
        
        #here we now directly access the IntVars we created with the controls 
        #to get the values.  Everything in the dictionary passed to 
        #the state manager is now is automatically stored when we close
        #ReaChorder.
        velocity = self.velocity.get()
        selectNote = self.highlight.get()
        self.msg("wtf")
        channel = self.channel.get()

        #get the list of notes in a chord by directing looking up ChordDict
        #with the name of the chord
        for j, vm in enumerate(self.rc.ChordDict[chord]):
            self.msg(str(j) + str(vm) + str(self.rc.ChordDict[chord]))
##            Reaper.ShowConsoleMsg(str(vm) + "\n") # + str(self.rc.ChordDict[chord]))
            #if j == self.rc.pChordName or j == self.beatsInBar - 1 : break #don't parse chordname and do 3 notes per bar for 3/4
            if j % randNote == 0:
                self.msg('--- draw note, random length 0.5, 1, 2')
                rpos = randPos[randint(0,2)]

                rlen = randLength[randint(0,2)]
                self.msg('--- rpos rlen set')

                # this is the original melody
                firstNotePosInChord = randint(0, 2)

                # harmony for "3 note chords"
                if firstNotePosInChord == 0:
                    secondNotePosInChord = 1
                    thirdNotePosInChord = 2

                elif firstNotePosInChord == 1:
                    secondNotePosInChord = 2
                    thirdNotePosInChord = 0

                else:
                    secondNotePosInChord = 0
                    thirdNotePosInChord = 1

                # add random extra note - set probability from the Melody tab
                r = randint(0, 100)
                if r < int(self.extraNoteProb.get()):
                    randExtraNote = True
                else:
                    randExtraNote = False

                # draw melody
                RSMidi.addNote(midiTake, int(channel), int(velocity), int(currentPos + rpos), int(self.rc.ChordDict[chord][firstNotePosInChord]),\
                                    int(self.rc.quartNoteLength * rlen), selectNote)

                if harmony1:
                    # "humanize"
                    harmony1Pos = rpos + randint(-60, 60)
                    if harmony1Pos < 0:
                        harmony1Pos = 0
                    velocity1 = velocity * 0.8
                    # draw "harmony"1
                    RSMidi.addNote(midiTake, int(channel), int(velocity1), int(currentPos + harmony1Pos), int(self.rc.ChordDict[chord][secondNotePosInChord]),\
                                        int(self.rc.quartNoteLength * rlen), selectNote)
                if harmony2:
                    # "humanize"
                    harmony2Pos = rpos + randint(-60, 60)
                    if harmony2Pos < 0:
                        harmony2Pos = 0
                    velocity2 = velocity * 0.8
                    # draw "harmony" 2
                    RSMidi.addNote(midiTake, int(channel), int(velocity2), int(currentPos + harmony2Pos), int(self.rc.ChordDict[chord][thirdNotePosInChord]),\
                                        int(self.rc.quartNoteLength * rlen), selectNote)

                currentPos += rpos + (self.rc.quartNoteLength * rlen)
                if randExtraNote:
                    RSMidi.addNote(midiTake, int(channel), int(velocity), int(currentPos + rpos), int(self.rc.ChordDict[chord][randint(0, 2)]),\
                                   int(self.rc.quartNoteLength * rlen), selectNote)
            else:
                RSMidi.addNote(midiTake, int(channel), int(velocity), int(currentPos), int(vm), \
                               int(self.rc.quartNoteLength), selectNote)
                currentPos += self.rc.quartNoteLength

        self.msg('drawMelody - Exit')
        return currentPos


    
    def init_widgets(self):
        # Widget Initialization

        self._label_1 = tkinter.Label(self.parent,
            text = "Draw:",bg="#E8E8E8"
        )
        self._label_2 = tkinter.Label(self.parent,
            text = "Highlight:",bg="#E8E8E8"
        )
        self._label_3 = tkinter.Label(self.parent,
            text = "Channel:",bg="#E8E8E8"
        )
        self._label_4 = tkinter.Label(self.parent,
            text = "Velocity:",bg="#E8E8E8"
        )
        ''''
        self._label_5 = tkinter.Label(self.parent,
            text = "Seed:",
        )
        '''
        self._label_6 = tkinter.Label(self.parent,
            text = "Extra note prob.",bg="#E8E8E8"
        )
       
        #here we use one of the state manager methods which returns an IntVar already 
        #with a callback to a method that updates the settings dictionary for this
        #class instance/section.  Now when the control is changed, the IntVar changes
        #and it is stored all at the same time.
        self.drawOrNot = self.newControlIntVar("draw", 1)
        self.cDrawOrNot = tkinter.Checkbutton(self.parent, variable=self.drawOrNot,bg="#E8E8E8")

        self.highlight = self.newControlIntVar("highlight", 0)
        self.cHighlight = tkinter.Checkbutton(self.parent, variable=self.highlight,bg="#E8E8E8")
        
        
        #same here.  Notice that we can use the returned IntVar as the textvariable for
        #the label, so that updates itself too.  (now go up and look in DrawMelody)
        self.channel = self.newControlIntVar("channel", 2)
        self.sChannel = tkinter.Scale(self.parent, from_=1, to=16, resolution=1, showvalue=0, orient="horizontal",\
                                      variable=self.channel)
        self.scaleTxt1 = ttk.Label(self.parent, textvariable=self.channel)
        
        self.velocity = self.newControlIntVar("velocity", 96)
        self.sVelocity = tkinter.Scale(self.parent, from_=1, to=127, resolution=1, showvalue=0, orient="horizontal",\
                                       variable=self.velocity)
        self.scaleTxt2 = ttk.Label(self.parent, textvariable=self.velocity)
        
        self.extraNoteProb = self.newControlIntVar("extranoteprob", 50)
        self.sExtraNoteProb = tkinter.Scale(self.parent, from_=0, to=100, resolution=1, showvalue=0, orient="horizontal",\
                                            variable=self.extraNoteProb)
        self.scaleTxt3 = ttk.Label(self.parent, textvariable=self.extraNoteProb)
        

        '''
        self.MelodyTypeSel = ttk.Combobox(self.parent, values=self.rc.MelodyType, state='readonly', width=13)
        self.MelodyTypeSel.current(0)
        '''

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
        '''
        self._label_5.grid(
            in_    = self.parent,
            column = 1,
            row    = 5,
            columnspan = 1,
            ipadx = 10,
            ipady = 0,
            padx = 0,
            pady = 10,
            rowspan = 1,
            sticky = "w"
        )
        '''
        self._label_6.grid(
            in_    = self.parent,
            column = 1,
            row    = 5,
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
        self.scaleTxt3.grid(
            in_    = self.parent,
            column = 2,
            row    = 5,
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

        '''
        self.MelodyTypeSel.grid(
            in_    = self.parent,
            column = 2,
            row    = 5,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )
        '''

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
        self.sExtraNoteProb.grid(
            in_    = self.parent,
            column = 2,
            row    = 5,
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