# from reaper_python import *
from rs_midi import RSMidi
import reaChord_data
import tkinter
from tkinter import ttk, X, Y, BOTH, RAISED, SUNKEN, HORIZONTAL, VERTICAL, CENTER, BOTTOM, TOP, ALL
from rs_statemanager import RSStateManager

# Canvas settings

SQUARE = 10
PAD = 5
PADY = 12
SIDE = SQUARE + PAD
SIDEY = SQUARE + PADY
ROWS = 5
COLS = 5
BG_FILL = 'gray90'
SEL_FILL = 'green'


class DrumSection(RSStateManager):

    def __init__(self, parent, rc):

        self.settings = {
            "draw": 0, "channel": 10
        }

        self.stateManager_Start("DrumSection", self.settings)
        self.msg("Drum __init__  Enter")
        #self.sta
        self.parent = parent
        self.rc = rc
        self.init_widgets()
        self.msg("Drum __init__  Exit")
        self.checkItt = 0
        self.midiBank = [
            [], # 0 Tom 2
            [], # 1 Tom 1
            [], # 2 Splash
            [], # 3 Ride
            [], # 4 Hihat II
            [], # 5 Hihat I
            [], # 6 Snare
            [] # 7 Kick
        ]

    def draw(self, midiTake, song, sectionLength):
        #song dictionary contains full Structure and chords for the sections
        # ie Verse and Chorus at the moment.
        if not(self.drawOrNot.get()): return
        currentPos = 0

        for i, sect in enumerate(song["Structure"]):
            chords = song[str(sect)]
            chordLength = sectionLength / len(chords)
            for chord in chords:
                self.drawDrum(midiTake, chord, currentPos, chordLength)
                currentPos += chordLength
        return currentPos

    def drawDrum(self,midiTake, chord, currentPos, chordLength):

        self.msg('drawDrum- Enter')
        #Reaper.ShowConsoleMsg(self.midiBank)
        channel = self.channel.get()

        self.midiBank[0] = [int(i) for i in self.midiBank[0]]
        self.midiBank[1] = [int(i) for i in self.midiBank[1]]
        self.midiBank[2] = [int(i) for i in self.midiBank[2]]
        self.midiBank[3] = [int(i) for i in self.midiBank[3]]
        self.midiBank[4] = [int(i) for i in self.midiBank[4]]
        self.midiBank[5] = [int(i) for i in self.midiBank[5]]
        self.midiBank[6] = [int(i) for i in self.midiBank[6]]
        self.midiBank[7] = [int(i) for i in self.midiBank[7]]

        self.midiBank[0].sort()
        self.midiBank[1].sort()
        self.midiBank[2].sort()
        self.midiBank[3].sort()
        self.midiBank[4].sort()
        self.midiBank[5].sort()
        self.midiBank[6].sort()
        self.midiBank[7].sort()

        for i in range(8):

            arr = list(self.midiBank[i])

            try:
                if not arr:
                    pass
                else:

                    seqStep = int(int(chordLength / len(arr)) / 8)
                    rangeStep = 0

                    for n in range(31):
                        for e,elem in enumerate(arr):
                            try:
                                if  n == elem:
                                    RSMidi.addNote(midiTake, int(channel), 80, int(rangeStep), int(self.rc.generalMIDIMap[i][0]), 120, 0)
                                else:
                                    rangeStep += int(seqStep)
                            except:
                                pass
            except:
                pass
        self.msg('drawDrum- Exit')

        return currentPos

    def init_widgets(self):

        # Widget Initialization

        self.grid = ttk.Frame(self.parent,height=175)
        self.grid.pack(fill=BOTH, expand=1)
        self.c = tkinter.Canvas(borderwidth=1,height=175,bg="#A4A4A4")

        self.grid.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
        self.grid.grid_rowconfigure(2, weight = 0, minsize = 10, pad = 0)
        self.grid.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self.grid.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self.grid.grid_columnconfigure(3, weight = 0, minsize = 150, pad = 0)
        self.grid.grid_columnconfigure(4, weight = 0, minsize = 150, pad = 0)
        self.grid.grid_columnconfigure(5, weight = 0, minsize = 150, pad = 0)

        self.c.grid(in_=self.grid,
            column = 2,
            row    = 2,
            columnspan = 8,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 15,
            sticky = "news"
        )

        self.drawOrNot = self.newControlIntVar("draw", 1)
        self.cDrawOrNot = tkinter.Checkbutton(self.parent, variable=self.drawOrNot,bg="#D9D9D9")

        self.channel = self.newControlIntVar("channel", 2)
        self.sChannel = tkinter.Scale(self.parent, from_=1, to=16, resolution=1, showvalue=0, orient="horizontal", variable=self.channel)
        self.scaleTxt1 = ttk.Label(self.parent, textvariable=self.channel)

        self.drummer = ttk.Combobox(self.grid, state='readonly', values=self.rc.patternList, width=33)
        self.drummer.bind('<<ComboboxSelected>>', lambda event: self.drawSeq())
        self.drummer.current(0)

        self._label_1 = tkinter.Label(self.grid, text = "Draw:",bg="#D9D9D9"
        )
        self._label_4 = tkinter.Label(self.grid,
            text = "Tom 2",bg="#D9D9D9",font=("System 12"),
        )
        self._label_5 = tkinter.Label(self.grid,
            text = "Tom 1",bg="#D9D9D9",font=("System 12"),
        )
        self._label_6 = tkinter.Label(self.grid,
            text = "Splash",bg="#D9D9D9",font=("System 12"),
        )
        self._label_7 = tkinter.Label(self.grid,
            text = "Ride",bg="#D9D9D9",font=("System 12"),
        )
        self._label_8 = tkinter.Label(self.grid,
            text = "HH Cl.",bg="#D9D9D9",font=("System 12"),
        )
        self._label_9 = tkinter.Label(self.grid,
            text = "HH Op.",bg="#D9D9D9",font=("System 12"),
        )
        self._label_10 = tkinter.Label(self.grid,
            text = "Snare",bg="#D9D9D9",font=("System 12"),
        )
        self._label_11 = tkinter.Label(self.grid,
            text = "Kick",bg="#D9D9D9",font=("System 12"),
        )

        # Geometry Management


        self.sChannel.grid(
            in_    = self.grid,
            column = 3,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )
        self.scaleTxt1.grid(
            in_    = self.grid,
            column = 3,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 35,
            pady = 0,
            rowspan = 1,
            sticky = "e"
        )
        self.cDrawOrNot.grid(
            in_    = self.grid,
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
        self._label_1.grid(
            in_    = self.grid,
            column = 1,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 10,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )

        self._label_4.grid(
            in_    = self.grid,
            column = 1,
            row    = 2,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )
        self._label_5.grid(
            in_    = self.grid,
            column = 1,
            row    = 3,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )
        self._label_6.grid(
            in_    = self.grid,
            column = 1,
            row    = 4,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )
        self._label_7.grid(
            in_    = self.grid,
            column = 1,
            row    = 5,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )
        self._label_8.grid(
            in_    = self.grid,
            column = 1,
            row    = 6,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )
        self._label_9.grid(
            in_    = self.grid,
            column = 1,
            row    = 7,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )

        self._label_10.grid(
            in_    = self.grid,
            column = 1,
            row    = 8,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )
        self._label_11.grid(
            in_    = self.grid,
            column = 1,
            row    = 9,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nes"
        )


        self.drummer.grid(
            in_    = self.grid,
            column = 4,
            row    = 1,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "w"
        )

        for i in range(32): # create the columns

            x = PAD + ( i * SIDE)

            if i % 4:
                OUTL = 'white'
            else:
                OUTL = 'black'

            for j in range(8): # create the rows
                y = PAD + (j * SIDEY)
                name = '{},{}'.format(j,i)
                self.c.create_rectangle(x, y, x+SQUARE, y+SQUARE, outline=OUTL, fill=BG_FILL, tags=('chk1', name))

        self.c.tag_bind('all', '<1>', lambda evt, can=self.c: self.select_seq_step(can))


    def drawSeq(self):
        val = self.drummer.current()

        #for i in basicDrumPattern1[0]
        if val > 0:
            self.midiBank =  []
            self.midiBank = self.rc.DrumPatterns[val-1]

            # delete and redraw!
            self.c.delete(ALL)

            self.c = tkinter.Canvas(borderwidth=2,height=175,bg="#838383")

            self.grid.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
            self.grid.grid_rowconfigure(2, weight = 0, minsize = 10, pad = 0)
            self.grid.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
            self.grid.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
            self.grid.grid_columnconfigure(3, weight = 0, minsize = 150, pad = 0)
            self.grid.grid_columnconfigure(4, weight = 0, minsize = 150, pad = 0)
            self.grid.grid_columnconfigure(5, weight = 0, minsize = 150, pad = 0)

            self.c.grid(in_=self.grid,
               column = 2,
               row    = 2,
               columnspan = 8,
               ipadx = 0,
               ipady = 0,
               padx = 0,
               pady = 0,
               rowspan = 15,
               sticky = "news"
            )

            self.midiBank[0] = [int(i) for i in self.midiBank[0]]
            self.midiBank[1] = [int(i) for i in self.midiBank[1]]
            self.midiBank[2] = [int(i) for i in self.midiBank[2]]
            self.midiBank[3] = [int(i) for i in self.midiBank[3]]
            self.midiBank[4] = [int(i) for i in self.midiBank[4]]
            self.midiBank[5] = [int(i) for i in self.midiBank[5]]
            self.midiBank[6] = [int(i) for i in self.midiBank[6]]
            self.midiBank[7] = [int(i) for i in self.midiBank[7]]

            self.midiBank[0].sort()
            self.midiBank[1].sort()
            self.midiBank[2].sort()
            self.midiBank[3].sort()
            self.midiBank[4].sort()
            self.midiBank[5].sort()
            self.midiBank[6].sort()
            self.midiBank[7].sort()


            for i in range(32): # create the columns

                x = PAD + ( i * SIDE)

                if i % 4:
                    OUTL = 'white'
                else:
                    OUTL = 'black'


                for j in range(0,8): # create the rows

                    if len(self.midiBank[j]) >=1:

                        leny = len(self.midiBank[j])

                        for k in range(30):

                            try:
                                if i == self.midiBank[j][k]:
                                    y = PAD + (j * SIDEY)
                                    name = '{},{}'.format(j,i)
                                    if k == 30:
                                        self.c.create_rectangle(x, y, x+SQUARE, y+SQUARE, outline='black', fill=SEL_FILL, tags=('chk0', name, 'current'))
                                    else:
                                        self.c.create_rectangle(x, y, x+SQUARE, y+SQUARE, outline='black', fill=SEL_FILL, tags=('chk0', name))
                            except:
                                if i not in self.midiBank[j]:
                                    y = PAD + (j * SIDEY)
                                    name = '{},{}'.format(j,i)
                                    self.c.create_rectangle(x, y, x+SQUARE, y+SQUARE, outline=OUTL, fill=BG_FILL, tags=('chk1', name))

                    else:
                        y = PAD + (j * SIDEY)
                        name = '{},{}'.format(j,i)
                        self.c.create_rectangle(x, y, x+SQUARE, y+SQUARE, outline=OUTL, fill=BG_FILL, tags=('chk1', name))

            self.c.tag_bind('all', '<1>', lambda evt, can=self.c: self.select_seq_step(can))


    def select_seq_step(self, canvas):

        item = self.select_current_seq_step(canvas)
        tags = canvas.gettags('current')


        if tags[0] == 'chk1':
            canvas.itemconfigure(item, fill=SEL_FILL, outline='black', tags=('chk0', tags[1], tags[2]))
        else:
            check = tags[1].split(",")
            if int(check[1]) % 4:
                OUTL = 'white'
            else:
                OUTL = 'black'
            canvas.itemconfigure(item, fill=BG_FILL, outline=OUTL, tags=('chk1', tags[1], tags[2]))

        for t in tags:
            if t not in ('current', 'chk0', 'chk1', 'text'):
                fill = t.split(",")
                if fill[1] in self.midiBank[int(fill[0])]:
                    if tags[0] == 'chk0':
                        idx = self.midiBank[int(fill[0])].index(fill[1])
                        self.midiBank[int(fill[0])].pop(idx)
                else:
                    self.midiBank[int(fill[0])].append(fill[1])
                    self.midiBank[int(fill[0])].sort()
        #Reaper.ShowConsoleMsg(self.midiBank)

    def select_current_seq_step(self, c):
        item = c.find_withtag('current')
        tags = c.gettags('current')
        if 'text' in tags:
            item = c.find_below(item)
        return item

    def msg(self, m):
        if (reaChord_data.debug):
            Reaper.ShowConsoleMsg(str(m)+'\n')