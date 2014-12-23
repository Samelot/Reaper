import beyond.Reaper

# from reaper_python import *

import sys

from wizard_section import Wizard
from chord_section import ChordSection
from bass_section import BassSection
from drum_section import DrumSection
from melody_section import MelodySection
from rs_statemanager import RSStateManager
sys.argv=["Main"]

import tkinter
from tkinter import ttk, Y, BOTH, RAISED

# from sws_python import *
from contextlib import contextmanager

from reaChord_data import RC, msg

from rs_midi import RSMidi

from reaper_track import Track, Item

try:
    import platform
except:
    pass
try:
    import os
except:
    pass

#########################################################################################################################################


class ReaChord(RSStateManager):
    '''
    ReaChorder main window/class.

    We create the objects that control the different sections here.  The only control that
    does anything here is the Draw Midi button which then calls all the other objects.

    Beforehand, the Proposed Song Progression was not stored, so the chorus was still random.

    Now, in the "Wizard" we store it in the "song" dictionary, which is initialised below.

    It's format is.. "V": ["Em","G", "C", "C"], Structure": "VCCVCVC"     (plus "C"horus obviously)

    We now pass this dictionary around to all the other sections so they know what the song
    structure is and can look up the chord notes directly by name of chord in the new ChordDict
    found in reaChord_data.

    REMOVED/TODO:  - save recall of settings
                   - region drawing
    '''

    def __init__(self, root):
        RSStateManager.appname = "ReaChorder"
        #create the empty song dictionary
        self.song = {}

        self.msg('__init__')
        self.stateManager_Start("Main", self.song)
        self.root = root
        self.root.title('ReaChorder')
        self.root.wm_attributes("-topmost", 1)

        self.img = None
        frame_height = 310

        try:
            osVersion = platform.release()
            if osVersion == 'XP':
                frame_width = 650 # WinXP
            else:
                frame_width = 650 # Win7+
        except:
            frame_width = 650 # Win7+

        self.mainFrame = ttk.Frame(self.root, width=frame_width, borderwidth=0, height=frame_height)
        self.mainFrame.pack(fill=BOTH, expand=1)

        self.rc = RC()  #init this b4 widgets so they can get tuples from it

        #tabbed GUI, using Notebook
        self.tabs = ttk.Notebook(self.mainFrame)
        self.tabs.pack(fill=BOTH, expand=Y, padx=10, pady=10)

        #add tabs with a Frame - one for each section
        self.frameWizard = ttk.Frame(self.tabs, borderwidth=0, \
                                     width=frame_width, height=frame_height)
        self.tabs.add(self.frameWizard, text="Wizard")

        #this creates an object of the Wizard type and stores it in self.wizard, calling its _init_
        #method in the process.  We can now access stuff using self.wizard.wizardyshizzle
        #we are passing it references to rc and song so that can read and write to them and use
        #their methods.
        self.wizard = Wizard(self.frameWizard, self.rc, self.song)

        #self.frameSongEditor = ttk.Frame(self.tabs, borderwidth=0, relief="sunken", width=740,height=255)
        #self.tabs.add(self.frameSongEditor, text="Song Editor")
        #TODO:  create song editor

        # the magic button
        self.btns = ttk.Button(self.frameWizard,  text='Draw into MIDI take...', width='20')
        self.btns.bind('<Button-1>', lambda event: self.drawMidi())

        self.btns.grid(
            in_    = self.frameWizard,
            column = 2,
            row    = 7,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 10,
            rowspan = 1,
            sticky = "e"
        )

        #we now create a list to store the objects for drawable sections we are about to create.
        #In drawMidi further down we iterate through the list calling all of their draw() methods
        #so if we want to add/remove sections, we only need to do it here.
        self.sections = []


        self.frameChords = ttk.Frame(self.tabs, borderwidth=0, width=650,height=245)
        self.tabs.add(self.frameChords, text="Chords")
        self.chords = ChordSection(self.frameChords, self.rc)
        self.sections.append(self.chords)

        self.frameMelody = ttk.Frame(self.tabs, borderwidth=0, width=650,height=245)
        self.tabs.add(self.frameMelody, text="Melody")
        self.melody = MelodySection(self.frameMelody, self.rc)
        self.sections.append(self.melody)

        self.frameBass = ttk.Frame(self.tabs, borderwidth=0, width=650,height=245)
        self.tabs.add(self.frameBass, text="Bass")
        self.bass = BassSection(self.frameBass, self.rc)
        self.sections.append(self.bass)

        self.frameDrum = ttk.Frame(self.tabs, borderwidth=0, width=650,height=245)
        self.tabs.add(self.frameDrum , text="Drum")
        self.drum = DrumSection(self.frameDrum, self.rc)
        self.sections.append(self.drum)

        # center the window
        w = frame_width
        h = 310
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(width=0, height=0)
        style = ttk.Style()
        style.theme_use('alt') 



    def close(self):
        global root
        root.destroy()



    def drawMidi(self):
        
        Reaper.OnConnectExecute = "from sws_python import *"

        with Reaper:

            quartNoteLength = 960
            self.msg('ReaChorder - drawMidi - Enter')
            p, bpm, bpi = Reaper.GetProjectTimeSignature2(0, 0, 0)
            bps = bpm/60
            beatsInBar = bpi
            barsPerSection = 4
            RSMidi.selAllNotes()
            RSMidi.deleteSelectedNotes()
            sectionLength = quartNoteLength * beatsInBar * barsPerSection

            take = RSMidi.getActTakeInEditor()

            if take == "(MediaItem_Take*)0x00000000" or take == "(MediaItem_Take*)0x0000000000000000":
                Reaper.ShowConsoleMsg("ReaChorder: Please open an item in the MIDI Editor first.\n")
            else:
                item = Item()   # init Item class
                itemId = Reaper.GetMediaItemTake_Item(take)    # get parent item
                songLength = sectionLength * len(self.song["Structure"])    # works (currently) :)
                item.setMidiItemLength(itemId, songLength, bps, quartNoteLength)
                item.setName(itemId, "ReaChorder Song")

                midiTake = RSMidi.allocateMIDITake(take)

                #go throught the sections, calling the draw() methods
                for obj in self.sections:
                    self.msg("wtf3")
                    p = obj.draw(midiTake, self.song, sectionLength)

                RSMidi.freeMIDITake(midiTake)



    def msg(self, m):
        msg(m)

###############################################
###############################################

# if __name__ == '__main__':
@ProgramStartDirect
def Main():
    root = tkinter.Tk()
    ReaChord(root)
    root.mainloop()

