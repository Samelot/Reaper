import os
import sys
import beyond.Reaper
##from reaper_python import *
##sys.argv=["Main"]

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox as msgBox

from Arpeggiator_functions import *

patternsPath = os.path.join(sys.path[0], "Patterns.txt")
patternsRemovedItems = os.path.join(sys.path[0], "Patterns_removed items.txt")
chordsPath = os.path.join(sys.path[0], "Chords.txt")
chordsRemovedItems = os.path.join(sys.path[0], "Chords_removed items.txt")
selectionsPath = os.path.join(sys.path[0], "Selections.txt")
selectionsRemovedItems = os.path.join(sys.path[0], "Selections_removed items.txt")

class Application:

    patternViewItemIdL = []
    chordViewItemIdL = []
    selectionViewItemIdL = []
##    treeItemId = "" # for re-ordering
##    noItemSel = 0   # for re-ordering
    noteList = ['0  C-1', '1  C#-1', '2  D-1', '3  D#-1', '4  E-1', '5  F-1', '6  F#-1', '7  G-1', '8  G#-1', '9  A-1', '10  A#-1', '11  B-1', '12  C0', '13  C#0', '14  D0', '15  D#0', '16  E0', '17  F0', '18  F#0', '19  G0', '20  G#0', '21  A0', '22  A#0', '23  B0', '24  C1', '25  C#1', '26  D1', '27  D#1', '28  E1', '29  F1', '30  F#1', '31  G1', '32  G#1', '33  A1', '34  A#1', '35  B1', '36  C2', '37  C#2', '38  D2', '39  D#2', '40  E2', '41  F2', '42  F#2', '43  G2', '44  G#2', '45  A2', '46  A#2', '47  B2', '48  C3', '49  C#3', '50  D3', '51  D#3', '52  E3', '53  F3', '54  F#3', '55  G3', '56  G#3', '57  A3', '58  A#3', '59  B3', '60  C4', '61  C#4', '62  D4', '63  D#4', '64  E4', '65  F4', '66  F#4', '67  G4', '68  G#4', '69  A4', '70  A#4', '71  B4', '72  C5', '73  C#5', '74  D5', '75  D#5', '76  E5', '77  F5', '78  F#5', '79  G5', '80  G#5', '81  A5', '82  A#5', '83  B5', '84  C6', '85  C#6', '86  D6', '87  D#6', '88  E6', '89  F6', '90  F#6', '91  G6', '92  G#6', '93  A6', '94  A#6', '95  B6', '96  C7', '97  C#7', '98  D7', '99  D#7', '100  E7', '101  F7', '102  F#7', '103  G7', '104  G#7', '105  A7', '106  A#7', '107  B7', '108  C8', '109  C#8', '110  D8', '111  D#8', '112  E8', '113  F8', '114  F#8', '115  G8', '116  G#8', '117  A8', '118  A#8', '119  B8', '120  C9', '121  C#9', '122  D9', '123  D#9', '124  E9', '125  F9', '126  F#9', '127  G9']
##    noteList = ['127  G9', '126  F#9', '125  F9', '124  E9', '123  D#9', '122  D9', '121  C#9', '120  C9', '119  B8', '118  A#8', '117  A8', '116  G#8', '115  G8', '114  F#8', '113  F8', '112  E8', '111  D#8', '110  D8', '109  C#8', '108  C8', '107  B7', '106  A#7', '105  A7', '104  G#7', '103  G7', '102  F#7', '101  F7', '100  E7', '99  D#7', '98  D7', '97  C#7', '96  C7', '95  B6', '94  A#6', '93  A6', '92  G#6', '91  G6', '90  F#6', '89  F6', '88  E6', '87  D#6', '86  D6', '85  C#6', '84  C6', '83  B5', '82  A#5', '81  A5', '80  G#5', '79  G5', '78  F#5', '77  F5', '76  E5', '75  D#5', '74  D5', '73  C#5', '72  C5', '71  B4', '70  A#4', '69  A4', '68  G#4', '67  G4', '66  F#4', '65  F4', '64  E4', '63  D#4', '62  D4', '61  C#4', '60  C4', '59  B3', '58  A#3', '57  A3', '56  G#3', '55  G3', '54  F#3', '53  F3', '52  E3', '51  D#3', '50  D3', '49  C#3', '48  C3', '47  B2', '46  A#2', '45  A2', '44  G#2', '43  G2', '42  F#2', '41  F2', '40  E2', '39  D#2', '38  D2', '37  C#2', '36  C2', '35  B1', '34  A#1', '33  A1', '32  G#1', '31  G1', '30  F#1', '29  F1', '28  E1', '27  D#1', '26  D1', '25  C#1', '24  C1', '23  B0', '22  A#0', '21  A0', '20  G#0', '19  G0', '18  F#0', '17  F0', '16  E0', '15  D#0', '14  D0', '13  C#0', '12  C0', '11  B-1', '10  A#-1', '9  A-1', '8  G#-1', '7  G-1', '6  F#-1', '5  F-1', '4  E-1', '3  D#-1', '2  D-1', '1  C#-1', '0  C-1']
##    a = "".join([str(i) + "\n" for i in noteList])
##    print(a)
    lastSelected = ""   # last selected item in "patterns" tab

    def __init__(self, root):
        Reaper.OnConnectExecute = "from sws_python import *"
        self.root = root
        self.root.wm_attributes("-topmost", 1)
        self.root.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
        self.rootWidth = 500
        self.rootHeight = 320
        self.root.geometry("%dx%d+100+100" % (self.rootWidth, self.rootHeight))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.bind("<Button-3>", self.popup)

        # make all container frames
        self.makeContainers()

        # populate treeviews
        self.nb.select(0)
        self.populateView("patternView", patternsPath)
        self.populateView("chordView", chordsPath)
        self.populateView("selectionView", selectionsPath)

        self.root.update_idletasks()

        self.showEditor.set(False)  # show/hide editor at start up
        self.showHideEditor()
        self.showSettings.set(True)    # show/hide (note)settings at start up
        self.showHideSettings()

    def makeContainers(self):   # container frames
        # parent frame for all widgets
        self.cFrameP = ttk.Frame(self.root)
        self.cFrameP.grid(sticky=(N,W,E,S), row=0, column=0)    #, columnspan=30)
        self.cFrameP.grid_columnconfigure(1, weight=1)
##        self.cFrameP.grid_columnconfigure(1, weight=1)
        self.cFrameP.grid_rowconfigure(0, weight=1)

        # container frame for notebook (treeviews)
        self.cFrameNb = ttk.Frame(self.cFrameP)
        self.cFrameNb.grid(sticky=(N,W,E,S), row=0, column=1, columnspan=30)
        self.cFrameNb.grid_columnconfigure(1, weight=1)
        self.cFrameNb.grid_rowconfigure(0, weight=1)

        # container (label)frame for entry (editor) widgets
        self.cFrameEdit = ttk.Labelframe(self.cFrameP, text="Editor")
##        self.cFrameEdit = ttk.Frame(self.cFrameP)
##        self.cFrameEdit.grid(sticky=(N,W,E,S), row=1, column=0, pady=3) #, columnspan=30)
        self.cFrameEdit.grid_columnconfigure(0, weight=1)

        # container frame for extra widgets
        self.cFrameExtra = ttk.Frame(self.cFrameP)
##        self.cFrameEdit = ttk.Frame(self.cFrameP)
        self.cFrameExtra.grid(sticky=(N,W,E,S), row=0, column=0, pady=3, rowspan=30)
##        self.aas= ttk.Button(self.cFrameExtra)
##        self.aas.grid(row=2, column=1)
##        self.cFrameExtra.grid_columnconfigure(0, weight=1)

##        # labelFrame around buttons
##        self.buttonLabelFrame = ttk.Labelframe(self.cFrameP)    #, text="Buttons")
##        self.buttonLabelFrame.grid(row=2, column=1, columnspan=100, padx=2, pady=2, sticky=(N,W,E,S))

        # container (label)frame for buttons
        self.cFrameButtons = ttk.Labelframe(self.cFrameP, text="MIDI editor controllers")
##        self.cFrameButtons = ttk.Frame(self.cFrameP)
        self.cFrameButtons.grid(sticky=(N,S,W,E), row=2, column=1, pady=4)#, columnspan=30)
##        self.cFrameButtons.grid_columnconfigure(0, weight=1, minsize=45)

##        self.cFrameButtons.grid_columnconfigure(1, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(2, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(3, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(4, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(5, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(6, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(7, weight=1, minsize=45)
##        self.cFrameButtons.grid_columnconfigure(8, weight=1, minsize=45)

##        #sizegrip for parent frame
##        self.sizeGrip = ttk.Sizegrip(self.cFrameP)
##        self.sizeGrip.grid(sticky=(E,S), row=10, column=10) #, columnspan=30, pady = 4)

##        self.cFrameButtons = ttk.Frame(self.cFrameP)
##        self.cFrameButtons.grid(sticky=(N,W,E,S), row=2, column=1, columnspan=30)

        # container frame for info/error -labels
        self.cFrameInfo = ttk.Frame(self.cFrameP)
        self.cFrameInfo.grid(sticky=(N,W,E,S), row=3, column=1) #, columnspan=30)
        self.cFrameInfo.grid_columnconfigure(0, weight=1)
        self.makeNoteBook()

    def makeNoteBook(self): # notebook (treeviews)
        self.nb = ttk.Notebook(self.cFrameNb)
        self.nb.grid(sticky=(N,W,E,S), column=1, row=0, columnspan=30)
        self.nb.bind("<<NotebookTabChanged>>", self.tabChanged)
        self.makeEditor()

    def makeEditor(self):   # editor edit boxes
        self.cFrameEntry = ttk.Frame(self.cFrameEdit)
        self.cFrameEntry.grid(sticky=(N,W,E,S), row=0, column=0) #, columnspan=30)
        self.cFrameEntry.grid_columnconfigure(0, weight=1, minsize=120)
        self.cFrameEntry.grid_columnconfigure(2, weight=6, minsize=40)
        self.cFrameEntry.grid_columnconfigure(4, weight=1, minsize=45)
        self.cFrameEntry.grid_columnconfigure(5, weight=1, minsize=45)

        # editor edit boxes
        self.patternNameBox = ttk.Entry(self.cFrameEntry)
        self.patternNameBox.grid(row=0, column=0, sticky=(N,W,E,S))

        self.patternBox = ttk.Entry(self.cFrameEntry, width=50)
        self.patternBox.grid(row=0, column=2, sticky=(N,W,E,S)) #, columnspan=30)

        self.offSet1 = ttk.Entry(self.cFrameEntry, width=3)
        self.offSet1.grid(row=0, column=1, sticky=(N,W,E,S)) #, columnspan=30)

        self.offSet2 = ttk.Entry(self.cFrameEntry, width=3)
        self.offSet2.grid(row=0, column=3, sticky=(N,W,E,S)) #, columnspan=30)

        # editor scroll bar
        self.patternBoxScroll = ttk.Scrollbar(self.cFrameEntry, orient=HORIZONTAL, command=self.patternBox.xview)
        self.patternBox['xscrollcommand'] = self.patternBoxScroll.set
        self.patternBoxScroll.grid(row=1, column=2, sticky=(N,W,E,S))

        # editor buttons

        # "apply changes (to selected item in tree view)" -button
        self.editBtnApply = ttk.Button(self.cFrameEntry, text="Apply", command=self.applyChangesToTreeItem)
        self.editBtnApply.grid(column=4, row=0, sticky=(W,E))
        self.editBtnApply.bind("<Enter>", lambda event: self.info.set("Apply pattern (from edit box) to selected item in treeview"))
        self.editBtnApply.bind("<Leave>", lambda event: self.updateInfoText())

        # "append pattern/name to list" -button
        self.editBtnAppend = ttk.Button(self.cFrameEntry, text="Append", command=self.appendToTreeView)
        self.editBtnAppend.grid(column=5, row=0, sticky=(W,E))
        self.editBtnAppend.bind("<Enter>", lambda event: self.info.set("Append pattern to treeview (from edit box)"))
        self.editBtnAppend.bind("<Leave>", lambda event: self.updateInfoText())

        # "get pattern from MIDI editor" -button
        self.editBtnGet = ttk.Button(self.cFrameEntry, text="Get", command=self.getPatternME)
        self.editBtnGet.grid(column=4, row=1, sticky=(W,E))
        self.editBtnGet.bind("<Enter>", lambda event: self.info.set("Get pattern from MIDI editor (selected notes)"))
        self.editBtnGet.bind("<Leave>", lambda event: self.updateInfoText())

        # "delete item from tree view" -button
        self.editBtnDel = ttk.Button(self.cFrameEntry, text="Delete", command=self.delItemFromTreeView)
        self.editBtnDel.grid(column=5, row=1, sticky=(W,E))
        self.editBtnDel.bind("<Enter>", lambda event: self.info.set("Delete selected item from treeview"))
        self.editBtnDel.bind("<Leave>", lambda event: self.updateInfoText())
        self.makeRightClickMenu()

    def makeRightClickMenu(self):   # popup menu (right click)
        self.showEditor = IntVar()
        self.showSettings = IntVar()
        self.RightClickMenu = Menu(self.root, tearoff=0)
        self.RightClickMenu.add_checkbutton(label="Show editor", variable=self.showEditor, command=self.showHideEditor)
        self.RightClickMenu.add_checkbutton(label="Show note settings", variable=self.showSettings, command=self.showHideSettings)
##        self.RightClickMenu.add_command(label="Save current view to file", command=self.save)
        self.RightClickMenu.add_separator()
        self.RightClickMenu.add_command(label="Open ReaScale file", command=self.reaScaleFileParser)
        self.RightClickMenu.add_separator()
        self.RightClickMenu.add_command(label="Clear treeview", command=lambda: self.clearView(self.getTabName(), True))
        self.RightClickMenu.add_separator()
        self.RightClickMenu.add_command(label="Load pattern file", command=self.openPatternFile)
        self.RightClickMenu.add_command(label="Save current view to file as...", command=self.save)

##        self.showEditor.set(False)  # show/hide editor at start up
##        self.showSettings.set(True)    # show/hide editor at start up
        self.makeCBoxRootNote()

    def makeCBoxRootNote(self): # combobox (root note)
        cBoxContainerCol = 0
        cBoxContainerRow = 1
        cBoxLabelCol = 0
        cBoxLabelRow = 0
        cBoxCol = 0
        cBoxRow = 1

        # container frame for combobox and transpose buttons
        self.cFrameCombo = ttk.Frame(self.cFrameButtons)
        self.cFrameCombo.grid(sticky=(N,W,E,S), row=cBoxContainerRow, column=cBoxContainerCol) #, columnspan=30)
##        self.cFrameCombo.grid_columnconfigure(0, weight=1, minsize=40)
##        self.cFrameCombo.grid_columnconfigure(1, weight=1, minsize=40)

        # label for root combobox
        self.label2 = ttk.Label(self.cFrameCombo, text="Root:")
        self.label2.grid(column=cBoxLabelCol, row=cBoxLabelRow, sticky=(W), columnspan=2)

        # label for transpose btns
        self.lblTransPose = ttk.Label(self.cFrameCombo, text="Transpose:")
        self.lblTransPose.grid(column=0, row=2, sticky=(W), columnspan=2)

        # combobox for root note selection
        self.boxValue = StringVar()
        self.box = ttk.Combobox(self.cFrameCombo, textvariable=self.boxValue, state='readonly', width=7)
        self.box['values'] = ['127  G9', '126  F#9', '125  F9', '124  E9', '123  D#9', '122  D9', '121  C#9', '120  C9', '119  B8', '118  A#8', '117  A8', '116  G#8', '115  G8', '114  F#8', '113  F8', '112  E8', '111  D#8', '110  D8', '109  C#8', '108  C8', '107  B7', '106  A#7', '105  A7', '104  G#7', '103  G7', '102  F#7', '101  F7', '100  E7', '99  D#7', '98  D7', '97  C#7', '96  C7', '95  B6', '94  A#6', '93  A6', '92  G#6', '91  G6', '90  F#6', '89  F6', '88  E6', '87  D#6', '86  D6', '85  C#6', '84  C6', '83  B5', '82  A#5', '81  A5', '80  G#5', '79  G5', '78  F#5', '77  F5', '76  E5', '75  D#5', '74  D5', '73  C#5', '72  C5', '71  B4', '70  A#4', '69  A4', '68  G#4', '67  G4', '66  F#4', '65  F4', '64  E4', '63  D#4', '62  D4', '61  C#4', '60  C4', '59  B3', '58  A#3', '57  A3', '56  G#3', '55  G3', '54  F#3', '53  F3', '52  E3', '51  D#3', '50  D3', '49  C#3', '48  C3', '47  B2', '46  A#2', '45  A2', '44  G#2', '43  G2', '42  F#2', '41  F2', '40  E2', '39  D#2', '38  D2', '37  C#2', '36  C2', '35  B1', '34  A#1', '33  A1', '32  G#1', '31  G1', '30  F#1', '29  F1', '28  E1', '27  D#1', '26  D1', '25  C#1', '24  C1', '23  B0', '22  A#0', '21  A0', '20  G#0', '19  G0', '18  F#0', '17  F0', '16  E0', '15  D#0', '14  D0', '13  C#0', '12  C0', '11  B-1', '10  A#-1', '9  A-1', '8  G#-1', '7  G-1', '6  F#-1', '5  F-1', '4  E-1', '3  D#-1', '2  D-1', '1  C#-1', '0  C-1']
        self.box.current(67)
        self.box.bind("<<ComboboxSelected>>", self.cBoxSelected)
        self.box.bind("<Enter>", self.setCboxFocused)
        self.box.grid(column=cBoxCol, row=cBoxRow, sticky=(W,E), columnspan=2)

##        self.btnTransposeUp = ttk.Button()
        self.btnTransposeUp = ttk.Button(self.cFrameCombo, text="U", width=3, command=lambda: self.transPScale("UP"))
        self.btnTransposeUp.grid(column=0, row=3, sticky=(W,E))
        self.btnTransposeUp.bind("<Enter>", lambda event: self.info.set("Transpose up to next note in scale"))
        self.btnTransposeUp.bind("<Leave>", lambda event: self.updateInfoText())

##        self.btnTransposeDown = ttk.Button()
        self.btnTransposeDown = ttk.Button(self.cFrameCombo, text="D", width=3, command=lambda: self.transPScale("DOWN"))
        self.btnTransposeDown.grid(column=1, row=3, sticky=(W,E))
        self.btnTransposeDown.bind("<Enter>", lambda event: self.info.set("Transpose down to prev. note in scale"))
        self.btnTransposeDown.bind("<Leave>", lambda event: self.updateInfoText())

        self.makePlayNavigateBtns()

    def makePlayNavigateBtns(self): # play/navigate
        playBtnContainerCol = 2
        playBtnContainerRow = 1
        playBtnLabelCol = 0
        playBtnLabelRow = 0
        playBtnCol = 0
        playBtnRow = 1
        cursorLBtnCol = 0
        cursorLBtnRow = 2
        cursorRBtnCol = 1
        cursorRBtnRow = 2

        #container frame for play/navigate
        self.cFramePlay = ttk.Frame(self.cFrameButtons)
##        self.cFramePlay = ttk.Labelframe(self.cFrameButtons, text="Play/navig.")
        self.cFramePlay.grid(sticky=(N,W,E,S), row=playBtnContainerRow, column=playBtnContainerCol) #, columnspan=30
        self.cFramePlay.grid_columnconfigure(0, weight=1, minsize=45)
        self.cFramePlay.grid_columnconfigure(1, weight=1, minsize=45)

        # label for play/navigate
        self.label2 = ttk.Label(self.cFramePlay, text="Play/navigate:")
        self.label2.grid(column=playBtnLabelCol, row=playBtnLabelRow, columnspan=2, sticky=(N))

        # play/stop button
        self.button3 = ttk.Button(self.cFramePlay, text="Play", command=lambda: playStop())
        self.button3.grid(column=playBtnCol, row=playBtnRow, columnspan=2, sticky=(W,E))

        # move cursor left
        self.button4 = ttk.Button(self.cFramePlay, text="<", width=3) # command=lambda: cursorLeftbyGrid())
        self.button4.grid(column=cursorLBtnCol, row=cursorLBtnRow, sticky=(W,E))
        self.button4.bind('<Button-1>', lambda event: cursorLeftbyGrid())
        self.button4.bind('<Control-Button-1>', lambda event: cursorStartOfCurrMeas())
        self.button4.bind("<Enter>", lambda event: self.info.set("Left click = 'Move cursor left by grid' - Ctrl+left click = 'Move to start of current/prev. measure'"))
        self.button4.bind("<Leave>", lambda event: self.updateInfoText())
##        self.button4.bind('<Control-Button-1>', self.leftByMeas)

        # move cursor right
        self.button5 = ttk.Button(self.cFramePlay, text=">", width=3) #, command=lambda: cursorRightbyGrid())
        self.button5.grid(column=cursorRBtnCol, row=cursorRBtnRow, sticky=(W,E))
        self.button5.bind('<Button-1>', lambda event: cursorRightbyGrid())
        self.button5.bind('<Control-Button-1>', lambda event: cursorStartOfNextMeas())
        self.button5.bind("<Enter>", lambda event: self.info.set("Left click = 'Move cursor right by grid' - Ctrl+left click = 'Move to start of next measure'"))
        self.button5.bind("<Leave>", lambda event: self.updateInfoText())

        # move cursor left (start of selection or item start)
        self.btnMoveStart = ttk.Button(self.cFramePlay, text="<<", width=3) #, command=lambda: cursorRightbyGrid())
        self.btnMoveStart.grid(column=0, row=3, sticky=(W,E))
        self.btnMoveStart.bind('<Button-1>', lambda event: cursorToStartOfSel())
##        self.btnMoveStart.bind('<Control-Button-1>', lambda event: cursorToStartOfItem())
        self.btnMoveStart.bind("<Enter>", lambda event: self.info.set("Move cursor to start of selection"))
        self.btnMoveStart.bind("<Leave>", lambda event: self.updateInfoText())
##        self.button5.bind('<Control-Button-1>', self.rightByMeas)

        # move cursor right (end of selection or item end)
        self.btnMoveEnd = ttk.Button(self.cFramePlay, text=">>", width=3) #, command=lambda: cursorRightbyGrid())
        self.btnMoveEnd.grid(column=1, row=3, sticky=(W,E))
        self.btnMoveEnd.bind('<Button-1>', lambda event: cursorToEndOfSel())
##        self.btnMoveEnd.bind('<Control-Button-1>', lambda event: cursorToEndOfItem())
        self.btnMoveEnd.bind("<Enter>", lambda event: self.info.set("Move cursor to end of selection"))
        self.btnMoveEnd.bind("<Leave>", lambda event: self.updateInfoText())



        self.makeApplyBtns()

    def makeApplyBtns(self):    # "apply" -buttons
        applyBtnsContainerCol = 1
        applyBtnsContainerRow = 1
        applyBtnsLabelCol = 0
        applyBtnsLabelRow = 0
        applyBtnsSelCol = 0
        applyBtnsSelRow = 1
        applyBtnsAllCol = 0
        applyBtnsAllRow = 2
        addBtnsCol = 0
        addBtnsRow = 2

        #container frame "apply" -buttons
        self.cFrameApply = ttk.Frame(self.cFrameButtons) # ttk.Labelframe(self.cFrameButtons, text="Apply/add")
        self.cFrameApply.grid(sticky=(N,W,E,S), row=applyBtnsContainerRow, column=applyBtnsContainerCol)    #, columnspan=30)
        self.cFrameApply.grid_columnconfigure(0, weight=0, minsize=45)

        # label for "apply" buttons
        self.applyLabel = ttk.Label(self.cFrameApply, text="Apply to/add:")
        self.applyLabel.grid(column=applyBtnsLabelCol, row=applyBtnsLabelRow, sticky=("W,E"))

        # "apply to selected notes" -button
        self.applyToSelBtn = ttk.Button(self.cFrameApply, text="Selected", command=lambda: self.applyPtrn(1))
        self.applyToSelBtn.grid(column=applyBtnsSelCol, row=applyBtnsSelRow, sticky=(W,E))
        self.applyToSelBtn.bind("<Enter>", lambda event: self.info.set("Apply selected pattern to selected notes"))
        self.applyToSelBtn.bind("<Leave>", lambda event: self.updateInfoText())
##        self.applyToSelBtn.bind('<Button-1>', self.applyToSelection)

        # "apply to all notes" -button
        self.applyToAllBtn = ttk.Button(self.cFrameApply, text="All", command=lambda: self.applyPtrn(0))
        self.applyToAllBtn.grid(column=applyBtnsAllCol, row=applyBtnsAllRow, sticky=(W,E))
        self.applyToAllBtn.bind("<Enter>", lambda event: self.info.set("Apply selected pattern to all notes"))
        self.applyToAllBtn.bind("<Leave>", lambda event: self.updateInfoText())

       # "add pattern to MIDI editor" -button
        self.addBtn = ttk.Button(self.cFrameApply, text="Add", command=self.addPtrn)
        self.addBtn.grid(column=addBtnsCol, row=addBtnsRow, sticky=(W,E))
        self.addBtn.bind("<Enter>", lambda event: self.info.set("Add selected pattern to REAPER MIDI editor"))
        self.addBtn.bind("<Leave>", lambda event: self.updateInfoText())
##        self.applyToAllBtn.bind('<Button-1>', self.applyToAll)
        self.makeChordBtns()

    def makeChordBtns(self):    # "add chord" -frame and button
        addChordBtnContainerCol = 1
        addChordBtnContainerRow = 1
        addChordBtnLabelCol = 0
        addChordBtnLabelRow = 0
        addChordBtnCol = 0
        addChordBtnRow = 1

        # container frame for "add chord" -button
        self.cFrameAddChord = ttk.Frame(self.cFrameButtons)
        self.cFrameAddChord.grid(sticky=(N,W,E,S), row=addChordBtnContainerRow, column=addChordBtnContainerCol) #, columnspan=30)

        # label for "add chord" button
        self.applyLabel = ttk.Label(self.cFrameAddChord, text="Add chord:")
        self.applyLabel.grid(column=addChordBtnLabelCol, row=addChordBtnLabelRow, sticky=("N"))

        # "add chord" -button
        self.addChordBtn = ttk.Button(self.cFrameAddChord, text="Add") #, command=lambda: addNote(Chords.Major))
        self.addChordBtn.bind('<Button-1>', self.addChord)
        self.addChordBtn.grid(column=addChordBtnCol, row=addChordBtnRow, sticky=(W))
        self.makeSelectBtns()

    def makeSelectBtns(self):   # "select" -buttons
        selBtnsContainerCol = 3
        selBtnsContainerRow = 1
        selBtnsLabelCol = 0
        selBtnsLabelRow = 0
        selBtnsSelCol = 0
        selBtnsSelRow = 1
        selBtnsUnSelCol = 0
        selBtnsUnSelRow = 2

        #container frame for "select" -buttons
        self.cFrameSelect = ttk.Frame(self.cFrameButtons)
        self.cFrameSelect.grid(sticky=(N,W,E,S), row=selBtnsContainerRow, column=selBtnsContainerCol) #, columnspan=30)

        # "label for "note selection/delete" -buttons
        self.noteSelLabel = ttk.Label(self.cFrameSelect, text="Select notes:")
        self.noteSelLabel.grid(column=selBtnsLabelCol, row=selBtnsLabelRow, sticky=(N))

        # selNotesbtn
        self.selNotesbtn = ttk.Button(self.cFrameSelect, text="All")
        self.selNotesbtn.grid(column=selBtnsSelCol, row=selBtnsSelRow, sticky=(W))
        with Reaper as r:
            self.selNotesbtn.bind('<Button-1>', lambda event: (r.Undo_BeginBlock2(0), selectAllNotes(), r.Undo_EndBlock2(0, "Select all notes", -1)))
##        self.selNotesbtn.bind('<Control-Button-1>', self.startOfNextMeas)

        # unSelNotesbtn
        self.unSelNotesbtn = ttk.Button(self.cFrameSelect, text="Unselect")
        self.unSelNotesbtn.grid(column=selBtnsUnSelCol, row=selBtnsUnSelRow, sticky=(W))
        self.unSelNotesbtn.bind('<Button-1>', lambda event: unSelectAllNotes())

        # select random notes -button
        self.selRandombtn = ttk.Button(self.cFrameSelect, text="Random")
        self.selRandombtn.grid(column=0, row=3, sticky=(W))
        self.selRandombtn.bind('<Button-1>', lambda event: selectRandomNotes())
##        self.unSelNotesbtn.bind('<Control-Button-1>', self.startOfNextMeas)
        self.makeFlipBtns()

    def makeFlipBtns(self):  # "flip" -buttons
        flipBtnsContainerCol = 4
        flipBtnsContainerRow = 1
        flipBtnsLabelCol = 0
        flipBtnsLabelRow = 0
        flipBtnsPosCol = 0
        flipBtnsPosRow = 1
        flipBtnsLenCol = 0
        flipBtnsLenRow = 2
        flipBtnsPitchCol = 0
        flipBtnsPitchRow = 3

        #container frame for "flip" -buttons
        self.cFrameFlip = ttk.Frame(self.cFrameButtons)
        self.cFrameFlip.grid(sticky=(N,W,E,S), row=flipBtnsContainerRow, column=flipBtnsContainerCol) #, columnspan=30)

        # "label for "flip" -buttons
        self.flipLabel = ttk.Label(self.cFrameFlip, text="Flip(reverse): ")
        self.flipLabel.grid(column=flipBtnsLabelCol, row=flipBtnsLabelRow, sticky=(N))

        # "flip Y-axis, don't change note length" -button
        self.flipHBtn = ttk.Button(self.cFrameFlip, text="Flip positions", command=lambda: flipSelNotes("POSITION"))
        self.flipHBtn.grid(column=flipBtnsPosCol, row=flipBtnsPosRow, sticky=(W))

        # "flip Y-axis, change note length" -button
        self.flipVBtn = ttk.Button(self.cFrameFlip, text="Flip lengths", command=lambda: flipSelNotes("LENGTH"))
        self.flipVBtn.grid(column=flipBtnsLenCol, row=flipBtnsLenRow, sticky=(W))

##        # "flip Y-axis, change note length" -button
        self.flipVBtn = ttk.Button(self.cFrameFlip, text="Flip pitches", command=lambda: flipSelNotes("PITCH"))
        self.flipVBtn.grid(column=flipBtnsPitchCol, row=flipBtnsPitchRow, sticky=(W))
        self.makeDeleteBtns()

    def makeDeleteBtns(self):   # "delete selected notes" -button
        delBtnContainerCol = 5
        delBtnContainerRow = 1
        delBtnLabelCol = 0
        delBtnLabelRow = 0
        delBtnCol = 0
        delBtnRow = 1

        #container frame for "delete" -button
        self.cFrameDel = ttk.Frame(self.cFrameButtons)
        self.cFrameDel.grid(sticky=(N,W,E,S), row=delBtnContainerRow, column=delBtnContainerCol) #, columnspan=30)

        # "label for "delete" -button
        self.delLabel = ttk.Label(self.cFrameDel, text="Delete notes:")
        self.delLabel.grid(column=delBtnLabelCol, row=delBtnLabelRow, sticky=(N))

        # "delete selected notes" -button
        self.delBtn = ttk.Button(self.cFrameDel, text="Delete sel")
        self.delBtn.grid(column=delBtnCol, row=delBtnRow, sticky=(W))
        self.delBtn.bind('<Button-1>', lambda event: deleteSelectedNotes())

        # "Undo" -button
        self.undoBtn = ttk.Button(self.cFrameDel, text="Undo")
        self.undoBtn.grid(column=0, row=4, sticky=(S))
        self.undoBtn.bind('<Button-1>', lambda event: undo())
        self.makeInversionBtns()

    def makeInversionBtns(self): # "inversion" -buttons

        invBtnsUCol = 0
        invBtnsURow = 2
        invBtnsDCol = 0
        invBtnsDRow = 3

        # "invert up" -button
        self.selNotesbtn = ttk.Button(self.cFrameAddChord, text="Inv up", command=lambda: invertChord("Up"))
        self.selNotesbtn.grid(column=invBtnsUCol, row=invBtnsURow, sticky=(W))

        # "invert down" -button
        self.unSelNotesbtn = ttk.Button(self.cFrameAddChord, text="Inv Down", command=lambda: invertChord("Down"))
        self.unSelNotesbtn.grid(column=invBtnsDCol, row=invBtnsDRow, sticky=(W))
        self.makeTreeViews()

    def makeTreeViews(self): # tree widgets

        # pattern view
        self.patternview = ttk.Treeview(self.nb, columns=["Notes","Pattern","All notes in selected pattern in selected root"], displaycolumns=["Notes","Pattern","All notes in selected pattern in selected root"] ,selectmode="browse", show="tree headings")
        self.patternview.column("#0", stretch="False", width=150)
        self.patternview.column("Notes",  anchor="center", width=40, stretch="False")
        self.patternview.column("Pattern", width=250)
        self.patternview.column("All notes in selected pattern in selected root", width=250)

        self.patternview.heading("Notes", text="Notes", anchor="w")
        self.patternview.heading("Pattern", text="Pattern", anchor="w")
        self.patternview.heading("All notes in selected pattern in selected root", text="All notes in selected pattern in selected root", anchor="w")
        self.patternview.heading("#0", text="Name") # , command = self.headingClicked)

##        self.patternview.bind('<Double-Button-1>', self.doubleLeft)
        self.patternview.grid(column=0, row=0, columnspan=30, sticky=(N,W,E,S))
        self.patternview.bind('<<TreeviewSelect>>', self.itemSelected)
        self.patternview.bind("<Enter>", self.focusPatternView)
##        self.patternview.bind("<ButtonPress-1>", self.buttonDown)
##        self.patternview.bind("<ButtonRelease-1>", self.buttonUp, add='+')
##        self.patternview.bind("<B1-Motion>", self.buttonDownMove, add='+')

        # chord view
        self.chordview = ttk.Treeview(self.nb, columns=["Notes","Pattern","All notes in selected pattern in selected root"], displaycolumns=["Notes","Pattern","All notes in selected pattern in selected root"] ,selectmode="browse", show="tree headings")
##        self.chordview = ttk.Treeview(self.nb, columns=["Notes","Pattern"], displaycolumns=["Notes","Pattern"] ,selectmode="browse", show="tree headings")
        self.chordview.column("#0", stretch="False", width=150)
        self.chordview.column("Notes", width=40, anchor="center", stretch="False")
        self.chordview.column("Pattern", width=250)
        self.chordview.column("All notes in selected pattern in selected root", width=250)

        self.chordview.heading("Notes", text="Notes", anchor="w")
        self.chordview.heading("Pattern", text="Pattern", anchor="w")
        self.chordview.heading("All notes in selected pattern in selected root", text="All notes in selected pattern in selected root", anchor="w")
        self.chordview.heading("#0", text="Name") # , command = self.headingClicked)

##        self.chordview.bind('<Double-Button-1>', self.doubleLeft)
        self.chordview.grid(column=0, row=0, columnspan=30, sticky=(N,W,E,S))
        self.chordview.bind('<<TreeviewSelect>>', self.itemSelected)
        self.chordview.bind("<Enter>", self.focusChordView)

        # selection view
        self.selectionview = ttk.Treeview(self.nb, columns=["Length","Pattern"], displaycolumns=["Length","Pattern"] ,selectmode="browse", show="tree headings")
        self.selectionview.column("#0", stretch="False", width=150)
        self.selectionview.column("Length", width=40, anchor="center", stretch="False")
        self.selectionview.column("Pattern", width=250)

        self.selectionview.heading("Length", text="Length", anchor="w")
        self.selectionview.heading("Pattern", text="Pattern", anchor="w")
        self.selectionview.heading("#0", text="Name") # , command = self.headingClicked)

##        self.selectionview.bind('<Double-Button-1>', self.applySelection)
        self.selectionview.grid(column=0, row=0, columnspan=30, sticky=(N,W,E,S))
        self.selectionview.bind('<<TreeviewSelect>>', self.itemSelected)
        self.selectionview.bind("<Enter>", self.focusSelectionView)

##        # scales view
##        self.scalesView = ttk.Treeview(self.nb, columns=["Notes","Pattern"], displaycolumns=["Notes","Pattern"] ,selectmode="browse", show="tree headings")
##        self.scalesView.column("#0", stretch="False", width=150)
##        self.scalesView.column("Notes",  anchor="center", width=40, stretch="False")
##        self.scalesView.column("Pattern", width=250)
##
##        self.scalesView.heading("Notes", text="Notes", anchor="w")
##        self.scalesView.heading("Pattern", text="Pattern", anchor="w")
##        self.scalesView.heading("#0", text="Name") # , command = self.headingClicked)
##
####        self.patternview.bind('<Double-Button-1>', self.doubleLeft)
##        self.scalesView.grid(column=0, row=0, columnspan=30, sticky=(N,W,E,S))
##        self.scalesView.bind('<<TreeviewSelect>>', self.itemSelected)
##        self.scalesView.bind("<Enter>", self.focusPatternView)
##        self.patternview.bind("<ButtonPress-1>", self.buttonDown)
##        self.patternview.bind("<ButtonRelease-1>", self.buttonUp, add='+')
##        self.patternview.bind("<B1-Motion>", self.buttonDownMove, add='+')

        # create pages (add treeviews to tabs)
        self.nb.add(self.patternview, text="Patterns", sticky="NWES")
        self.nb.add(self.chordview, text="Chords", sticky="NWES")
        self.nb.add(self.selectionview, text="Selector", sticky="NWES")
##        self.nb.add(self.scalesView, text="Scales", sticky="NWES")
        self.makeInfoLabel()

    def makeInfoLabel(self):    # info/error label
        # info label
        self.info = StringVar()
        self.infolabel = ttk.Label(self.cFrameInfo, textvariable=self.info)
        self.infolabel.grid(column=0, row=0, sticky=(W,E)) # ,columnspan=30 )

        # error label
        self.error = StringVar()
        self.errorLabel = ttk.Label(self.cFrameInfo, textvariable=self.error, background="RED")
##        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
        self.errorLabel.bind('<Button-1>', self.removeErrorLabel)
        self.makeScrollBars()

    def makeScrollBars(self):# scrollbars

        # scrollbar for pattern view
        self.sBar1 = ttk.Scrollbar(self.cFrameNb, orient=VERTICAL, command=self.patternview.yview)
##        self.sBar1.grid(column=5, row=0, sticky=(N,S))
        self.patternview['yscrollcommand'] = self.sBar1.set

        # scrollbar for chord view
        self.sBar2 = ttk.Scrollbar(self.cFrameNb, orient=VERTICAL, command=self.chordview.yview)
##        self.sBar2.grid(column=5, row=0, sticky=(N,S))
        self.chordview['yscrollcommand'] = self.sBar2.set

        # scrollbar for selection view
        self.sBar3 = ttk.Scrollbar(self.cFrameNb, orient=VERTICAL, command=self.selectionview.yview)
##        self.sBar2.grid(column=5, row=0, sticky=(N,S))
        self.selectionview['yscrollcommand'] = self.sBar3.set

        self.makeSettingsWidget(0, 2, 0, 1, 3)

    # settings
    def makeSettingsWidget(self, parentFrameCol, noteLengthLFrameRow, channelLFrameRow, velocityLFrameRow, positionLFrameRow):
        # container for "settings" widgets
        self.settingsFrame = ttk.Frame(self.cFrameExtra)
##        self.settingsFrame.grid(row=0, column=0, padx=2, pady=2, sticky=(N,W,E,S))
        self.settingsFrame.grid(row=0, rowspan = 100, column=5, padx=2, pady=2, sticky=(N,W,E,S))

        # label frame for "note length" combobox
        self.lFrameLength = ttk.Labelframe(self.settingsFrame, text="Note length")
        self.lFrameLength.grid(row=noteLengthLFrameRow, column=parentFrameCol, padx=2, pady=2, sticky=(N,W,E,S))

        # label frame for "channel" combobox
        self.lFrameChannel = ttk.Labelframe(self.settingsFrame, text="Channel")
        self.lFrameChannel.grid(row=channelLFrameRow, column=parentFrameCol, padx=2, pady=2, sticky=(N,W,E,S))

        # label frame for "velocity" combobox
        self.lFrameVelocity = ttk.Labelframe(self.settingsFrame, text="Velocity")
        self.lFrameVelocity.grid(row=velocityLFrameRow, column=parentFrameCol, padx=2, pady=2, sticky=(N,W,E,S))

##        # label frame for "position" combobox
##        self.lFramePos = ttk.Labelframe(self.settingsFrame, text="Position")
##        self.lFramePos.grid(row=positionLFrameRow, column=parentFrameCol, padx=2, pady=2, sticky=(N,W,E,S))

        # label frame for "harmonize" comboboxes/button
        self.lFrameHarmonize = ttk.Labelframe(self.settingsFrame, text="Harmonize")
        self.lFrameHarmonize.grid(row=positionLFrameRow, column=parentFrameCol, padx=2, pady=2, sticky=(N,W,E,S))

        # combobox for note length
        self.noteLenCBoxVal = StringVar()
        self.noteLenCBox = ttk.Combobox(self.lFrameLength, textvariable=self.noteLenCBoxVal, state='readonly', width=8)
        self.noteLenCBox['values'] = ['1/128', '1/64', '1/32', '1/16', '1/8', '1/4', '1/2', '1', '2', '3', '4']
        self.noteLenCBox.current(3)
        self.noteLenCBox.bind("<<ComboboxSelected>>", lambda event: self.getCBoxLengthValue)
##        self.box.bind("<Enter>", self.setCboxFocused)
        self.noteLenCBox.grid(column=0, row=0, sticky=(W))

        # button for "set length"
        self.btnSetLength = ttk.Button(self.lFrameLength, text="Set", width = 10, command=lambda: setProperty(self.getCBoxLengthValue(), "LENGTH"))
        self.btnSetLength.grid(column=0, row=1)#, sticky=(W))
        self.btnSetLength.bind("<Enter>", lambda event: self.info.set("Set new length for selected notes"))
        self.btnSetLength.bind("<Leave>", lambda event: self.updateInfoText())


        # combobox for channel selection
        self.cBoxChannelVal = StringVar()
        self.cBoxChannel = ttk.Combobox(self.lFrameChannel, textvariable=self.cBoxChannelVal, state='readonly', width=8)
        self.cBoxChannel['values'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
        self.cBoxChannel.current(0)
        self.cBoxChannel.bind("<<ComboboxSelected>>", lambda event: self.getCBoxChannelValue)
##        self.box.bind("<Enter>", self.setCboxFocused)
        self.cBoxChannel.grid(column=0, row=0, sticky=(W))

        # button for "set channel"
        self.btnSetChannel = ttk.Button(self.lFrameChannel, text="Set", width = 10, command=lambda: setProperty(self.getCBoxChannelValue(), "CHANNEL"))
        self.btnSetChannel.grid(column=0, row=1)#, sticky=(W))
        self.btnSetChannel.bind("<Enter>", lambda event: self.info.set("Set new channel for selected notes"))
        self.btnSetChannel.bind("<Leave>", lambda event: self.updateInfoText())

        # combobox for velocity
        self.cBoxVelocityVal = StringVar()
        self.cBoxVelocity = ttk.Combobox(self.lFrameVelocity, textvariable=self.cBoxVelocityVal, state='readonly', width=8)
        self.cBoxVelocity['values'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127']
        self.cBoxVelocity.current(95)
        self.cBoxVelocity.bind("<<ComboboxSelected>>", lambda event: self.getCBoxVelocityValue)
##        self.box.bind("<Enter>", self.setCboxFocused)
        self.cBoxVelocity.grid(column=0, row=0, sticky=(W))

        # button for "set new velocity"
        self.btnSetVelocity = ttk.Button(self.lFrameVelocity, text="Set", width = 10, command=lambda: setProperty(self.getCBoxVelocityValue(), "VELOCITY"))
        self.btnSetVelocity.grid(column=0, row=1)#, sticky=(W))
        self.btnSetVelocity.bind("<Enter>", lambda event: self.info.set("Set new velocity for selected notes"))
        self.btnSetVelocity.bind("<Leave>", lambda event: self.updateInfoText())

##        # button for "set new velocity"
##        self.chkBtnVel = ttk.Checkbutton(self.lFrameVelocity) #, text="Set")#, command=lambda: setProperty(self.getCBoxVelocityValue(), "VELOCITY"))
##        self.chkBtnVel.grid(column=1, row=0, sticky=(E))
##        self.btnSetVelocity.bind("<Enter>", lambda event: self.info.set("Set new velocity for selected notes"))
##        self.btnSetVelocity.bind("<Leave>", lambda event: self.updateInfoText())

##        # combobox for position
##        self.cBoxPositionVal = StringVar()
##        self.cBoxPosition = ttk.Combobox(self.lFramePos, textvariable=self.cBoxPositionVal, state='readonly', width=8)
##        self.cBoxPosition['values'] = ["Prev note end"]
##        self.cBoxPosition.current(0)
##        self.cBoxPosition.bind("<<ComboboxSelected>>", self.getCBoxPositionValue)
####        self.box.bind("<Enter>", self.setCboxFocused)
##        self.cBoxPosition.grid(column=0, row=0, sticky=(W))

##        # button for "set new position"
##        self.btnSetPos = ttk.Button(self.lFramePos, text="Set", width = 10, command=lambda: setProperty(self.getC(), "POSITION"))
##        self.btnSetPos.grid(column=0, row=1)#, sticky=(W))
##        self.btnSetPos.bind("<Enter>", lambda event: self.info.set("Set new position for selected notes"))
##        self.btnSetPos.bind("<Leave>", lambda event: self.updateInfoText())

##        # button for "set new position"
##        self.btnSetPos = ttk.Button(self.lFramePos, text="Set", width = 10, command=self.harmonize)
##        self.btnSetPos.grid(column=0, row=1)#, sticky=(W))
##        self.btnSetPos.bind("<Enter>", lambda event: self.info.set("Set new position for selected notes"))
##        self.btnSetPos.bind("<Leave>", lambda event: self.updateInfoText())

        # label frame for "harmonize" combobox1
        self.lblHNote1 = ttk.Label(self.lFrameHarmonize, text="1st Note")
        self.lblHNote1.grid(row=0, column=0, sticky=(N,W,E,S))

        # label frame for "harmonize" combobox2
        self.lblHNote1 = ttk.Label(self.lFrameHarmonize, text="2nd Note")
        self.lblHNote1.grid(row=0, column=1, sticky=(N,W,E,S))

        # combobox1 for "harmonize"
        self.cBoxHNote1Val = StringVar()
        self.cBoxHNote1 = ttk.Combobox(self.lFrameHarmonize, textvariable=self.cBoxHNote1Val, state='readonly', width=3)
        self.cBoxHNote1['values'] = ['-20', '-19', '-18', '-17', '-16', '-15', '-14', '-13', '-12', '-11', '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self.cBoxHNote1.current(20)
        self.cBoxHNote1.bind("<<ComboboxSelected>>", lambda event: self.getCBoxHNote1Value)
##        self.box.bind("<Enter>", self.setCboxFocused)
        self.cBoxHNote1.grid(column=0, row=2, sticky=(W))

        # combobox2 for "harmonize"
        self.cBoxHNote2Val = StringVar()
        self.cBoxHNote2 = ttk.Combobox(self.lFrameHarmonize, textvariable=self.cBoxHNote2Val, state='readonly', width=3)
        self.cBoxHNote2['values'] = ['-20', '-19', '-18', '-17', '-16', '-15', '-14', '-13', '-12', '-11', '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self.cBoxHNote2.current(20)
        self.cBoxHNote2.bind("<<ComboboxSelected>>", lambda event: self.getCBoxHNote2Value)
##        self.box.bind("<Enter>", self.setCboxFocused)
        self.cBoxHNote2.grid(column=1, row=2, sticky=(W))

        # button for "harmonize"
        self.btnHarmonize = ttk.Button(self.lFrameHarmonize, text="Harmonize", command=self.harmonize, width=10)
        self.btnHarmonize.grid(column=0, row=3, sticky=(N,S,W,E), columnspan=2)
        self.btnHarmonize.bind("<Enter>", lambda event: self.info.set("Harmonize selected notes"))
        self.btnHarmonize.bind("<Leave>", lambda event: self.updateInfoText())

##        # button for "set new velocity"
##        self.btnSetVelocity = ttk.Button(self.cFrameExtra, text="Harmonize", command=self.harmonize)
##        self.btnSetVelocity.grid(column=4, row=0, sticky=(N,S,W,E))
##        self.btnSetVelocity.bind("<Enter>", lambda event: self.info.set("Harmonize selected notes"))
##        self.btnSetVelocity.bind("<Leave>", lambda event: self.updateInfoText())


#    GUI functions    ##########################################################

    def patternLfromPatternText(self):
        """ Convert pattern(text) to list
            return patternL (if not indexerror) or patternL = []"""
        if self.getTabName() == "Selector":
            return
        try: # except indexerror (if nothing selected)
            sel = self.patternview.selection()[0]
            pattern = self.getTextFromSelView()[1]
            patternL = pattern.split(",")
            patternL = [int(str(x).strip()) for x in patternL] # convert to int
            return patternL

        except IndexError:
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Select 'Patterns' -tab -> select scale or pattern")
            patternL = []
            return patternL

    def getCBoxHNote1Value(self):
        return int(self.cBoxHNote1.get())

    def getCBoxHNote2Value(self):
        return int(self.cBoxHNote2.get())

    def harmonize(self):
        if not self.getTabName() == "Patterns":
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Select 'Patterns' -tab -> select scale")
            return
        try:
            if self.getTabName() == "Patterns":
                sel = self.patternview.selection()[0]
                hNote1 = self.getCBoxHNote1Value()
                hNote2 = self.getCBoxHNote2Value()
                length = self.getCBoxLengthValue()
                channel = self.getCBoxChannelValue()
                velocity = self.getCBoxVelocityValue()

                fullScaleText = str(self.patternview.item(sel, "values")[2])
                if "[" in fullScaleText:
                    fullScaleText = fullScaleText.replace("[", "")
                if "]" in fullScaleText:
                    fullScaleText = fullScaleText.replace("]", "")

                root = self.getRootFromCBox()

                fullScaleL = fullScaleText.split(",")
                fullScaleL = [int(str(char).strip()) for char in fullScaleL]# if int(char) <= 127]
                harmonizeSelected(root, hNote1, hNote2, fullScaleL, length, channel, velocity)

        except IndexError:# as e:
##            msg(e)
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Select 'Patterns' -tab -> select scale")

    def transPScale(self, direction):
        try:
            if self.getTabName() == "Patterns":
                sel = self.patternview.selection()[0]
                fullScaleText = str(self.patternview.item(sel, "values")[2])
                if "[" in fullScaleText:
                    fullScaleText = fullScaleText.replace("[", "")
                if "]" in fullScaleText:
                    fullScaleText = fullScaleText.replace("]", "")

                root = self.getRootFromCBox()

                fullScaleL = fullScaleText.split(",")
        ##                fullScaleL = [int(char) + root for char in fullScaleL if int(char) + root <= 127]
                fullScaleL = [int(str(char).strip()) for char in fullScaleL if int(char) <= 127]
                transPoseScale(root, fullScaleL, direction)

        except IndexError as e:
##            msg(e)
            pass

    def popup(self, event): # RightClickMenu to mousepos
        self.RightClickMenu.post(event.x_root, event.y_root)

    def populateView(self, view, path): # populate
        """ view = 'patternView', 'chordView', 'selectionView', 'scalesView' """
##        patternL =[]
        if view == "patternView":
            treeView = self.patternview
##            path = patternsPath
            idList = self.patternViewItemIdL
            patternCol = "Pattern"
            lengthCol = "Notes"

        elif view == "chordView":
            treeView = self.chordview
##            path = chordsPath
            idList = self.chordViewItemIdL
            patternCol = "Pattern"
            lengthCol = "Notes"

        elif view == "selectionView":
            treeView = self.selectionview
##            path = selectionsPath
##            idList = self.selectionViewItemIdL
            patternCol = "Pattern"
            lengthCol = "Length"

##        elif view == "scalesView":
##            treeView = self.selectionview
####            path = selectionsPath
####            idList = self.selectionViewItemIdL
##            patternCol = "Pattern"
##            lengthCol = "Notes"

##        if view != "patternView":
##            return

        if os.path.isfile(path):
            try:
                offSLen = 0
                with open(path, 'r') as f:
                    for line in f:
                        patternL =[]
                        if not "=" in line:
                            continue
                        patternName = line.split("=")[0].strip()
                        pattern = list(line.split("=")[1].strip())

                        pl = pattern.index("[")
                        del(pattern[pl])
                        pr = pattern.index("]")
                        del(pattern[pr])
                        pattern = "".join(pattern)
##                        patternLength = len(pattern.split(","))

                        a = pattern.split(",")
                        maxim = 1
                        for i in a:
                            if view == "selectionView":
                                patternL.append(str(i.strip()))
                                # count "offset" notes
                                if "u" in i:
                                    offSLen += int(i.strip()[1:])
                                elif int(i) > maxim:
                                    maxim = int(i)
                                patternLength = maxim + offSLen

                            elif view != "selectionView":
                                patternL.append(int(i.strip()))
                                patternLength = len(patternL)


##                        if view != "selectionView":

                        treeId = treeView.insert("", 'end', text=patternName)
                        if view == "patternView" or view == "chordView":
##                            # get "full scale" for pattern
##                            fullScale = self.makeFullScale(patternL)
                            idList.append(treeId)
##                            treeView.set(treeId, "All notes in selected pattern in selected root", fullScale)

##                        elif view == "chordView":
##                            self.chordViewItemIdL.append(treeId)
##                            treeView.set(treeId, "All notes in selected pattern in selected root", fullScale)
                        elif view == "selectionView":
                            self.selectionViewItemIdL.append(treeId)
                        treeView.set(treeId, patternCol, pattern)
                        treeView.set(treeId, lengthCol, patternLength)

                        offSLen = 0

            except (IOError, PermissionError) as e:
                msg(e)

##        else:
##            msg(str(path) + " not found")

    def makeFullScale(self, patternL):
        """return "full scale" from 0 to 127"""
        if self.getTabName == "Selector":
            return

        b = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119]
        aS = [10, 22, 34, 46, 58, 70, 82, 94, 106, 118]
        a = [9, 21, 33, 45, 57, 69, 81, 93, 105, 117]
        gS = [8, 20, 32, 44, 56, 68, 80, 92, 104, 116]
        g = [7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127]
        fS = [6, 18, 30, 42, 54, 66, 78, 90, 102, 114, 126]
        f = [5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 125]
        e = [4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124]
        dS = [3, 15, 27, 39, 51, 63, 75, 87, 99, 111, 123]
        d = [2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122]
        cS = [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121]
        c = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120]

        for j, pitch in enumerate(patternL):
            if self.getRootFromCBox() in b:
                patternL[j] -= 1
                noteOffSet = -1
            elif self.getRootFromCBox() in aS:
                patternL[j] -= 2
                noteOffSet = -2
            elif self.getRootFromCBox() in a:
                patternL[j] -= 3
                noteOffSet = -3
            elif self.getRootFromCBox() in gS:
                patternL[j] -= 4
                noteOffSet = -4
            elif self.getRootFromCBox() in g:
                patternL[j] -= 5
                noteOffSet = -5
            elif self.getRootFromCBox() in fS:
                patternL[j] -= 6
                noteOffSet = -6
            elif self.getRootFromCBox() in f:
                patternL[j] -= 7
                noteOffSet = -7
            elif self.getRootFromCBox() in e:
                patternL[j] -= 8
                noteOffSet = -8
            elif self.getRootFromCBox() in dS:
                patternL[j] -= 9
                noteOffSet = -9
            elif self.getRootFromCBox() in d:
                patternL[j] -= 10
                noteOffSet = -10
            elif self.getRootFromCBox() in cS:
                patternL[j] -= 11
                noteOffSet = -11

        fullScale = patternL[:]

##        fullScale = patternL[:]
##        fullScale = []

        if patternL:
            x = 0
            stopLoop = 0
            while x <= 1000:  ###############################
                for j, pitch in enumerate(patternL):

                    if pitch + 12 > 127:
                        stopLoop = 1
                        patternL = patternL[:j]
                        break

                    elif pitch + 12 == 127:
                        stopLoop = 1
                        patternL[j] = pitch + 12
                        patternL = patternL[:j + 1]
                        break
##                    else:
##                        if j <= len(patternL) - 1:
##                            print(j)
##                        patternL[j] = pitch
                    else:
                        patternL[j] = pitch + 12

                fullScale += patternL
                x += 1
                if stopLoop:    # break "while loop" if pitch >= 127
                    break

            # remove duplicates and order the list (ascending)
            fullScale = sorted(set(fullScale))
            fullScale = [x for x in fullScale if x >= 0]
##            print(fullScale)

            return fullScale



##    def buttonDown(self, event):
##        self.treeItemId = ""
####        self.noItemSel = 0
##
##        itemIdInRow = self.patternview.identify_row(event.y)
##        if itemIdInRow not in self.patternview.selection():
##            self.patternview.selection_set(itemIdInRow)
##
##            index = self.patternview.index(itemIdInRow)
####            print(index)
##            try:
####                a = self.patternview.yview()
####                print(a)
##                self.treeItemId =  self.patternview.selection()[0]
##                print(self.treeItemId)
##
####                self.firstItemX, firstItemY, firstItemW, firstItemH = self.patternview.bbox(self.patternViewItemIdL[0])
####                print(self.firstItemX)
####                Y = self.patternview.bbox(self.patternViewItemIdL[0])[0]
####                print(self.patternview.bbox(self.patternViewItemIdL[0])[0])
####                print(self.patternview.bbox(selected))
##            except IndexError:
####                self.noItemSel = 1
##                print("indexerror")
##                return
##
####            self.treeItemId ==
##
##    def buttonUp(self, event):
####        print(self.firstItemX)
##        if self.patternview.identify_row(event.y) in self.patternview.selection():
##            self.patternview.selection_set(self.patternview.identify_row(event.y))
##
##    def buttonDownMove(self, event):
##        print(event.y)
####        print(self.noItemSel)
####        print(self.patternViewItemIdL[0])
##        moveTo = self.patternview.index(self.patternview.identify_row(event.y))
####        print(self.patternview.identify_element(event.x, event.y))
####        print(self.patternview.identify_region(event.x, event.y))
##        for s in self.patternview.selection():
####                selected =  self.patternview.selection()[0]
##                element = self.patternview.identify_element(event.x, event.y)
##                region = self.patternview.identify_region(event.x, event.y)
####                if element != "text" or element != "padding":
##                if region == "nothing" and event.y > 40:
##                    moveTo = len(self.patternViewItemIdL) - 1
##
##                elif region == "nothing" and event.y < 10:
##                    moveTo = 0
##
####                if region == "nothing" and event.x < 2:
####                    moveTo = self.patternview.index(self.patternview.identify_row(event.y))
####
####                if region == "nothing" and event.x > 40:
####                    moveTo = self.patternview.index(self.patternview.identify_row(event.y))
##
####                print(self.patternview.bbox(selected))
##                self.patternview.move(s, '', moveTo)
####            print(moveTo)
####            if moveTo == 0: # len(self.patternViewItemIdL) - 1:
####                moveTo = len(self.patternViewItemIdL) - 1
####            self.patternview.move(s, '', moveTo)

    def showHideSettings(self):
        # root window size/pos
        w, h, x, y = self.root.winfo_width(), self.root.winfo_height(), self.root.winfo_rootx(), self.root.winfo_rooty()
        self.root.update_idletasks()

        if self.showSettings.get():
            # place "settings frame" to grid
            self.cFrameExtra.grid(row=0, column=0, padx=2, pady=2, sticky=(N,W,E,S))
##            self.settingsFrame.grid(row=0, rowspan = 100, column=0, padx=2, pady=2, sticky=(N,W,E,S))
            self.root.update_idletasks()
##            settingsFrameWidth = self.settingsFrame.winfo_width()
            settingsFrameWidth = self.cFrameExtra.winfo_width()
            # resize tk window
            self.root.geometry("%dx%d" % (w + settingsFrameWidth, h))
            self.setEditBoxText()
        else:
##            settingsFrameWidth = self.settingsFrame.winfo_width()
            settingsFrameWidth = self.cFrameExtra.winfo_width()
            self.cFrameExtra.grid_remove()
            self.root.update_idletasks()
            # resize tk window
            self.root.geometry("%dx%d" % (w - settingsFrameWidth, h))

    def showHideEditor(self):
        if self.showEditor.get():
            self.cFrameEdit.grid(sticky=(N,W,E,S), row=1, column=1, columnspan = 100) #, ipadx = 50, ipady=20)
            self.setEditBoxText()
        else:
            self.cFrameEdit.grid_remove()

    def getPatternME(self):
        with Reaper as r:
            octaveOffset = int(r.SNM_GetIntConfigVar("midioctoffs", -100) - 1)
            if octaveOffset == -100:
                msg("Couldn't get 'miditicksperbeat' from reaper.ini")
                return
            take = getActTakeInEditor()
            midiTake = allocateMIDITake(take)
##            r.ShowMessageBox(str(midiTake), "", 0)
            notesCount = int(r.FNG_CountMidiNotes(midiTake))
            if self.getTabName() != "Selector":
                rootNote = self.getRootFromCBox()
                pitchList = []
                for i in range(notesCount):
                    currNote = r.FNG_GetMidiNote(midiTake, i)
                    currSel = r.FNG_GetMidiNoteIntProperty(currNote, "SELECTED")
                    if currSel:
                        pitch = r.FNG_GetMidiNoteIntProperty(currNote, "PITCH")
                        pitchList.append(pitch + 12 * octaveOffset)

            elif self.getTabName() == "Selector":
                selectionL = []
                selStartFound = False
                unSelL = []
                uStartOffSet = 0
                uEndOffSet = 0

                for i in range(notesCount):
                    currNote = r.FNG_GetMidiNote(midiTake, i)
                    currSel = r.FNG_GetMidiNoteIntProperty(currNote, "SELECTED")
    ##                isMuted = FNG_GetMidiNoteIntProperty(currNote, "MUTED")

                    # count unselected notes before the selected notes
                    if not currSel and not selStartFound:
                        uStartOffSet += 1

                    # make pattern
                    elif currSel:
                        if not selStartFound:
                            selStartFound = True
                            firstSelNotePos = i
                        selectionL.append(i - firstSelNotePos + 1)
                        uEndOffSetStart = i

                        # if last note is selected -> uEndOffSet = 0
                        if i == notesCount - 1:
                            uEndOffSet = 0
    ##                    uEndOffSetStart += 1

                    # count unselected notes after the selected notes
                    elif not currSel and selStartFound:
                        if i < notesCount:
                            uEndOffSet = i - uEndOffSetStart

                if uStartOffSet > 0:
                    selectionL.insert(0, "u" + str(uStartOffSet))

                if uEndOffSet > 0:
                    selectionL.append("u" + str(uEndOffSet))


            r.FNG_FreeMidiTake(midiTake)

            if self.getTabName() == "Selector":
                patternText = "".join([str(noteNumber) + ", " for noteNumber in selectionL if not str(noteNumber).startswith("u")]).strip()
                self.offSet1.delete(0, END)
                self.offSet2.delete(0, END)
                self.offSet1.insert(0, uStartOffSet)
                self.offSet2.insert(0, uEndOffSet)
            else:
                patternText = "".join([str(int(noteNumber) - rootNote) + ", " for noteNumber in pitchList]).strip()
            self.patternBox.delete(0, END)
            self.patternBox.insert(0, patternText.rstrip(", "))

    def applyChangesToTreeItem(self):
        pitch = ""
        selTab = self.getTabName()
        startOffSet = 0
        endOffSet = 0

        if selTab == "Patterns":
            treeView = self.patternview
            idList = self.patternViewItemIdL
            patternCol = "Pattern"
            lengthCol = "Notes"

        elif selTab == "Chords":
            treeView = self.chordview
            idList = self.chordViewItemIdL
            patternCol = "Pattern"
            lengthCol = "Notes"

        elif selTab == "Selector":
            treeView = self.selectionview
            idList = self.selectionViewItemIdL
            patternCol = "Pattern"
            lengthCol = "Length"

        try: # except indexerror (if nothing selected)
            sel = treeView.selection()[0]
            pattern = self.patternBox.get() # get pattern from edit box
            patternL = pattern.split(",")
            # try to convert items in pattern list to int
            try:
                for i, value in enumerate(patternL):
                    patternL[i] = int(str(value).strip())
                    if not 0 <= abs(int(value)) <= 127 and selTab != "Selector":
                        self.error.set("Wrong value at index " + str(i + 1) + ": '" + value + "'\n" + "Values should be between -127 and 127")
                        return
                    elif selTab =="Selector" and int(value) <= 0:
                        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                        self.error.set("Wrong value at index " + str(i + 1) + ": '" + value + "'\n" + "Values should be > 0")
                        return

            # return if item is not integer and show errorlabel
            except ValueError:
                self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                self.error.set("Wrong type at index " + str(i + 1) + ": '" + value + "'")
                return

            # count the length of "selection pattern"
            if selTab == "Selector":
                maxim = int(max(patternL))
                print(patternL)

                startOffSet = self.offSet1.get()
                if startOffSet == "":
                    startOffSet = 0

                # try to get int values from "offset" entrys
                try:
                    startOffSet = int(startOffSet)
                    if startOffSet < 0:
                        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                        self.error.set("Pattern 'Start offset' - Use Positive integers (>0)")
                        return
                except ValueError:
                    self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                    self.error.set("Pattern 'Start offset' - Use Positive integers (>0)")
                    return

                endOffSet = self.offSet2.get()
                if endOffSet == "":
                    endOffSet = 0
                try:
                    endOffSet = int(endOffSet)
                    if endOffSet < 0:
                        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                        self.error.set("Pattern 'End offset' - Use Positive integers (>0)")
                        return

                except ValueError:
                    self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                    self.error.set("Pattern 'End offset' - Use Positive integers (>0)")
                    return

                if startOffSet and startOffSet != "0":
                    patternL.insert(0, startOffSet)
                    pattern = "u" + str(startOffSet) + ", " + pattern

                if endOffSet and endOffSet != "0":
                    patternL.append(endOffSet)
                    pattern = pattern + ", " + "u" + str(endOffSet)

                patternLen = int(startOffSet) + int(endOffSet) + maxim

            if selTab == "Patterns":
##                patternL = [int(x) for x in patternL] # convert to int
                # get "full scale" for pattern
                fullScale = self.makeFullScale(patternL)
                treeView.set(sel, "All notes in selected pattern in selected root", fullScale)

            treeView.item(sel, text=self.patternNameBox.get())

##            if selTab != "Selector":
##                treeView.set(sel, patternCol, pattern)

            treeView.set(sel, patternCol, pattern)
            if selTab != "Selector":
                treeView.set(sel, lengthCol, len(patternL))

            if selTab == "Selector":
                treeView.set(sel, lengthCol, patternLen)


        except IndexError: # as e:
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Nothing selected")
            return

    def appendToTreeView(self):
        pitch = ""
        selTab = self.getTabName()
        startOffSet = 0
        endOffSet = 0

        if selTab == "Patterns":
            treeView = self.patternview

        elif selTab == "Chords":
            treeView = self.chordview

        elif selTab == "Selector":
            treeView = self.selectionview

        try: # except indexerror (if nothing selected)
##            sel = treeView.selection()[0]
            pattern = self.patternBox.get() # get pattern from edit box
            patternL = pattern.split(",")
            # try to convert items in pattern list to int
            try:
                for i, value in enumerate(patternL):
                    patternL[i] = int(str(value).strip())
                    if not 0 <= abs(int(value)) <= 127 and selTab != "Selector":
                        self.error.set("Wrong value at index " + str(i + 1) + ": '" + value + "'\n" + "Values should be between -127 and 127")
                        return
                    elif selTab =="Selector" and int(value) <= 0:
                        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                        self.error.set("Wrong value at index " + str(i + 1) + ": '" + value + "'\n" + "Values should be > 0")
                        return

            # return if item is not integer and show errorlabel
            except ValueError:
                self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                self.error.set("Wrong type at index " + str(i + 1) + ": '" + value + "'")
                return

            # count the length of "selection pattern"
            if selTab == "Selector":
                maxim = int(max(patternL))
##                print(patternL)

                startOffSet = self.offSet1.get()
                if startOffSet == "":
                    startOffSet = 0

                # try to get int values from "offset" entrys
                try:
                    startOffSet = int(startOffSet)
                    if startOffSet < 0:
                        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                        self.error.set("Pattern 'Start offset' - Use Positive integers (>0)")
                        return
                except ValueError:
                    self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                    self.error.set("Pattern 'Start offset' - Use Positive integers (>0)")
                    return

                endOffSet = self.offSet2.get()
                if endOffSet == "":
                    endOffSet = 0
                try:
                    endOffSet = int(endOffSet)
                    if endOffSet < 0:
                        self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                        self.error.set("Pattern 'End offset' - Use Positive integers (>0)")
                        return

                except ValueError:
                    self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
                    self.error.set("Pattern 'End offset' - Use Positive integers (>0)")
                    return

                if startOffSet and startOffSet != "0":
                    patternL.insert(0, startOffSet)
                    pattern = "u" + str(startOffSet) + ", " + pattern

                if endOffSet and endOffSet != "0":
                    patternL.append(endOffSet)
                    pattern = pattern + ", " + "u" + str(endOffSet)

                patternLen = int(startOffSet) + int(endOffSet) + maxim

            # get "full scale" for pattern
            fullScale = self.makeFullScale(patternL)

            if self.getTabName() == "Patterns":
                treeId = self.patternview.insert("", 'end', text=self.patternNameBox.get())
                self.patternViewItemIdL.append(treeId)

                self.patternview.set(treeId, "Pattern", pattern)
                self.patternview.set(treeId, "Notes", len(patternL))
                self.patternview.set(treeId, "All notes in selected pattern in selected root", fullScale)
                self.patternview.selection_set(treeId)
                self.patternview.see(treeId)



            elif self.getTabName() == "Chords":
                treeId = self.chordview.insert("", 'end', text=self.patternNameBox.get())
                self.chordViewItemIdL.append(treeId)

                self.chordview.set(treeId, "Pattern", pattern)
                self.chordview.set(treeId, "Notes", len(patternL))
                self.chordview.selection_set(treeId)
                self.chordview.see(treeId)

                # get "full scale" for pattern
                fullScale = self.makeFullScale(patternL)

            elif self.getTabName() == "Selector":
                treeId = self.selectionview.insert("", 'end', text=self.patternNameBox.get())
                self.selectionViewItemIdL.append(treeId)

                self.selectionview.set(treeId, "Pattern", pattern)
                self.selectionview.set(treeId, "Length", patternLen)
                self.selectionview.selection_set(treeId)
                self.selectionview.see(treeId)

        except IndexError: # as e:
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Nothing selected")
            return

    def delItemFromTreeView(self):
        newLines = ""
        try:
            if self.getTabName() == "Patterns":
                sel = self.patternview.selection()[0]
                patternName = self.patternview.item(sel, "text")
                # remove extra whitespaces and add ", " between values
                patternL = [x.strip() for x in self.patternview.item(sel, "values")[1].split(",")]
                pattern = "".join([pitch + ", " for pitch in patternL])
                # remove the last ", "
                pattern = pattern.rstrip(", ")
                if patternName == "":
                    patternName = "No name"
                newLines = newLines + patternName + " = " + "[" + pattern + "]\n"

                for i, item in enumerate(self.patternViewItemIdL):
                    if item == sel:
                        try:
                            with open(patternsRemovedItems, 'a') as outFile:
                                outFile.write(newLines)
                            self.patternview.delete(sel)
                            del self.patternViewItemIdL[i]
                            break
                        except (IOError, PermissionError) as e:
                            msg(e)

            elif self.getTabName() == "Chords":
                sel = self.chordview.selection()[0]
                patternName = self.chordview.item(sel, "text")
                # remove extra whitespaces and add ", " between values
                patternL = [x.strip() for x in self.chordview.item(sel, "values")[1].split(",")]
                pattern = "".join([pitch + ", " for pitch in patternL])
                # remove the last ", "
                pattern = pattern.rstrip(", ")
                if patternName == "":
                    patternName = "No name"
                newLines = newLines + patternName + " = " + "[" + pattern + "]\n"

                for i, item in enumerate(self.chordViewItemIdL):
                    if item == sel:
                        try:
                            with open(chordsRemovedItems, 'a') as outFile:
                                outFile.write(newLines)
                            self.chordview.delete(sel)
                            del self.chordViewItemIdL[i]
                            break
                        except (IOError, PermissionError) as e:
                            msg(e)

            elif self.getTabName() == "Selector":
                sel = self.selectionview.selection()[0]
                patternName = self.selectionview.item(sel, "text")
                # remove extra whitespaces and add ", " between values
                patternL = [x.strip() for x in self.selectionview.item(sel, "values")[1].split(",")]
                pattern = "".join([x + ", " for x in patternL])
                # remove the last ", "
                pattern = pattern.rstrip(", ")
                if patternName == "":
                    patternName = "No name"
                newLines = newLines + patternName + " = " + "[" + pattern + "]\n"

                for i, item in enumerate(self.selectionViewItemIdL):
                    if item == sel:
                       try:
                            with open(selectionsRemovedItems, 'a') as outFile:
                                outFile.write(newLines)
                            self.selectionview.delete(sel)
                            del self.selectionViewItemIdL[i]
                            break
                       except (IOError, PermissionError) as e:
                            msg(e)

        except IndexError: # as e:
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Nothing selected")
            return

    def removeErrorLabel(self, event):
        self.errorLabel.grid_remove()

    def getTabName(self):
        return self.nb.tab("current", "text")

    def getTextFromSelView(self):
        try:
            if self.getTabName() == "Patterns":
                sel = self.patternview.selection()[0]
                treeText = self.patternview.item(sel, "text")
                textFromPatternCol = self.patternview.item(sel, "values")[1]
            elif self.getTabName() == "Chords":
                sel = self.chordview.selection()[0]
                treeText = self.chordview.item(sel, "text")
                textFromPatternCol = self.chordview.item(sel, "values")[1]
            elif self.getTabName() == "Selector":
                sel = self.selectionview.selection()[0]
                treeText = self.selectionview.item(sel, "text")
                textFromPatternCol = self.selectionview.item(sel, "values")[1]

        except IndexError: # as e:
            treeText = ""
            textFromPatternCol = ""

        return treeText, textFromPatternCol

    def setEditBoxText(self):
        offS1 = ""
        offS2 = ""
        notes = ""
        noteNumber = ""
        i = ""
        try:
##            t = self.getTextFromComboBox().split()[0]
            treeText, textFromPatternCol = self.getTextFromSelView()
            d = str(textFromPatternCol).split(",")
            if d != [""]:
                if d[0].strip().startswith("u"):
                    offS1 = d[0].strip()[1:]

                if d[-1].strip().startswith("u"):
                    offS2 = d[-1].strip()[1:]

                for i in d:
                    if not i.strip().startswith("u"):   # remove selector "offsets"
                        i = i.strip() + ", "
                        noteNumber += str(i)
            noteNumber = noteNumber.rstrip(", ")

            self.patternNameBox.delete(0, END)
            self.patternBox.delete(0, END)
            self.patternNameBox.insert(0, treeText)
            self.patternBox.insert(0, noteNumber)

            self.offSet1.delete(0, END)
            self.offSet2.delete(0, END)

            self.offSet1.insert(0, offS1)
            self.offSet2.insert(0, offS2)

        except TypeError as e:
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set(e)

    def updateInfoText(self):
        notes = ""
        try:
            cBoxText = self.getTextFromComboBox()
            treeText, textFromPatternCol = self.getTextFromSelView()
            if self.getTabName() == "Selector" or textFromPatternCol == "":
                self.info.set(treeText)
            else:
                rootNoteNumber = self.getTextFromComboBox().split()[0]
                patternL = str(textFromPatternCol).split(",")
                if patternL != [""]:
                    for noteNumber in patternL:
                        # get notes from noteList and update infotext
                        note = self.noteList[int(rootNoteNumber) + int(noteNumber)].split()[1]
                        notes += str(note) + str("-")
                    notes = notes.rstrip("-")
##                    self.info.set("(" + cBoxText + ")" + " " + notes)
                    self.info.set(notes)

        except IndexError:
            return

    def tabChanged(self, event):
        if self.getTabName() == "Patterns":
            self.sBar2.grid_remove()
            self.sBar3.grid_remove()
            self.cFrameAddChord.grid_remove()
            self.offSet1.grid_remove()
            self.offSet2.grid_remove()

            self.sBar1.grid(column=6, row=0, sticky=(N,S))
##            self.cFrameCombo.grid()
##            self.editBtnGet.grid(column=2, row=1, sticky=(W))
            self.addBtn.grid(column=0, row=3, sticky=(W))   # show "add pattern" button

        elif self.getTabName() == "Chords":
            self.sBar1.grid_remove()
            self.sBar3.grid_remove()
            self.addBtn.grid_remove()   # remove "add pattern" button
            self.offSet1.grid_remove()
            self.offSet2.grid_remove()

##            self.cFrameCombo.grid()
            self.cFrameAddChord.grid()
            self.sBar2.grid(column=6, row=0, sticky=(N,S))
##            self.editBtnGet.grid(column=2, row=1, sticky=(W))

        elif self.getTabName() == "Selector":
            self.sBar1.grid_remove()
            self.sBar2.grid_remove()
##            self.cFrameCombo.grid_remove()
            self.cFrameAddChord.grid_remove()
##            self.editBtnGet.grid_remove()
            self.addBtn.grid_remove()   # remove "add pattern" button
            self.offSet1.grid()
            self.offSet2.grid()
            self.sBar3.grid(column=6, row=0, sticky=(N,S))

        self.updateInfoText()

    def itemSelected(self, event):

##        self.lastSelected = sel
        self.upDateFullScale()

##        fullScale = self.makeFullScale(patternL)
##        self.patternview.set(sel, "All notes in selected pattern in selected root", fullScale)

        if self.showEditor.get():
            self.setEditBoxText()
        self.updateInfoText()

    def upDateFullScale(self):  # if selection changed or root changed
        if self.getTabName() != "Patterns":
            return
        try:
            sel = self.patternview.selection()[0]

            patternL = self.patternLfromPatternText()
            if patternL == []:
                return
            if self.lastSelected != "":
                self.patternview.set(self.lastSelected, "All notes in selected pattern in selected root", "")

            fullScale = self.makeFullScale(patternL)
            self.patternview.set(sel, "All notes in selected pattern in selected root", fullScale)
            self.lastSelected = sel

        except IndexError:
            print("Select pattern")


    def addChord(self, event):
        if len(self.chordViewItemIdL) == 0:
            msg("Empty list")
            return
        patternName, textFromPatternCol = self.getTextFromSelView()
        if not textFromPatternCol:
##            msg("No tree item selected")
##            print("No tree item selected")
            return
        rootNote = self.getRootFromCBox()    # get notenumber from combobox
        self.updateInfoText()
        patternL = [int(x) for x in textFromPatternCol.split(",")]

        length = self.getCBoxLengthValue()
        channel = self.getCBoxChannelValue()
        velocity = self.getCBoxVelocityValue()
##        print(length)

        addChordToEditCursor(patternL, rootNote, channel, length, velocity)

    def addPtrn(self):
        if not self.getTabName() == "Patterns":
            return
        patternName, textFromPatternCol = self.getTextFromSelView()
        if not textFromPatternCol:
##            msg("No tree item selected")
##            print("No tree item selected")
            return
        rootNote = self.getRootFromCBox()    # get notenumber from combobox
        self.updateInfoText()
        patternL = [int(str(x).strip()) for x in textFromPatternCol.split(",")]
        length = self.getCBoxLengthValue()
        channel = self.getCBoxChannelValue()
        velocity = self.getCBoxVelocityValue()

        addPattern(patternL, rootNote, channel, length, velocity)

    def applyPtrn(self, sel):
        patternName, textFromPatternCol = self.getTextFromSelView()

        if self.getTabName() == "Patterns":
            rootNote = self.getRootFromCBox()    # get notenumber from combobox
            self.updateInfoText()
            patternL = [int(str(x).strip()) for x in textFromPatternCol.split(",")]

            applyPattern(patternL, rootNote, sel)

        elif self.getTabName() == "Selector":
            offS1 = 0
            offS2 = 0
            self.updateInfoText()
            patternL = [str(x).strip() for x in textFromPatternCol.split(",")]
            if patternL[0].startswith("u"):
                offS1 = int(patternL[0][1:])
                patternL.pop(0)

            if patternL[-1].startswith("u"):
                offS2 = int(patternL[-1][1:])
                patternL.pop(-1)
##            print(patternL)
            if sel == 0:
                patternL = [int(x) for x in patternL]
                applyToAllNotes(patternL, offS1, offS2)
            elif sel == 1:
                patternL = [int(x) for x in patternL]
                applyToSelNotes(patternL, offS1, offS2)

    def save(self):
        scriptPath = str(sys.path[0])
##        print(scriptPath)
        filename = asksaveasfilename(initialdir = scriptPath, filetypes=[("txt files", "*.txt")], title="Save current treeview as", defaultextension=".txt")
        if filename == "":
            return
        newLines = ""
        patternL = []

        if self.getTabName() == "Patterns":
            try:
                with open(filename, 'w') as outFile:
                    for treeItem in self.patternViewItemIdL:
                        patternName = self.patternview.item(treeItem, "text")
                        # remove extra whitespaces
                        patternL = [x.strip() for x in self.patternview.item(treeItem, "values")[1].split(",")]
                        # list -> string and add ", " between values
                        pattern = "".join([pitch + ", " for pitch in patternL])
                        # remove the last ", "
                        pattern = pattern.rstrip(", ")
                        if patternName == "":
                            patternName = "No name"
                        newLines = newLines + patternName + " = " + "[" + pattern + "]\n"
                    outFile.write(newLines)
            except (IOError, PermissionError) as e:
                print(e)
##                msg(e)

        elif self.getTabName() == "Chords":
            try:
                with open(filename, 'w') as outFile:
                    for treeItem in self.chordViewItemIdL:
                        patternName = self.chordview.item(treeItem, "text")
                        pattern = self.chordview.item(treeItem, "values")[1]
                        if patternName == "":
                            patternName = "No name"
                        newLines = newLines + patternName + " = " + "[" + pattern + "]\n"
                    outFile.write(newLines)
            except (IOError, PermissionError) as e:
                print(e)
##                msg(e)

        elif self.getTabName() == "Selector":
            try:
                with open(filename, 'w') as outFile:
                    for treeItem in self.selectionViewItemIdL:
                        patternName = self.selectionview.item(treeItem, "text")
                        pattern = self.selectionview.item(treeItem, "values")[1]
                        if patternName == "":
                            patternName = "No name"
                        newLines = newLines + patternName + " = " + "[" + pattern + "]\n"
                    outFile.write(newLines)
            except (IOError, PermissionError) as e:
                print(e)
##                msg(e)

# root combobox

    def cBoxSelected(self, event):
        self.upDateFullScale()
        self.getTextFromComboBox()
        self.updateInfoText()

    # get text from "root combobox"
    def getTextFromComboBox(self):
        return str(self.box.get())

    # get root from "root combobox"
    def getRootFromCBox(self):
        return int(self.box.get().split()[0])

# settings - note length combobox

    def getCBoxLengthValue(self):
        l = self.noteLenCBox.get().split("/")
        if len(l) == 2:
            value = 1 / int(l[1])
        else:
            value = int(l[0])
        return value

# settings - channel combobox

    # get value from "channel combobox"
    def getCBoxChannelValue(self):
##        self.getCBoxChannelValue()
        return int(self.cBoxChannel.get())

# settings - velocity combobox

    def getCBoxVelocityValue(self):

##        print(type(self.cBoxVelocity.get()))
##        self.getCBoxChannelValue()
        return int(self.cBoxVelocity.get())

# settings - velocity combobox

    def getCBoxPositionValue(self):

##        print(type(self.cBoxVelocity.get()))
##        self.getCBoxChannelValue()
        return self.cBoxPosition.get()

##        self.updateInfoText()
    def setCboxFocused(self, event):
        self.box.focus_set()

    def focusPatternView(self, event):
        self.patternview.focus_set()

    def focusChordView(self, event):
        self.chordview.focus_set()

    def focusSelectionView(self, event):
        self.selectionview.focus_set()

    def reaScaleFileParser(self):
        if not self.getTabName() == "Patterns":
            self.errorLabel.grid(column=0, row=1, sticky=(W,E),columnspan=30)
            self.error.set("Works only in 'Patterns' -view")
            return

        pattern = "0, "
        patternCol = "Pattern"
        lengthCol = "Notes"
        patternL = []
        patternLength = 1

        scriptPath = str(sys.path[0])
        openfilename=askopenfilename(initialdir = scriptPath, filetypes=[("reascale files", "*.reascale")], title="Open ReaScale file")
        extension = os.path.splitext(openfilename)[1][1:].strip().lower()
        if openfilename and os.path.isfile(openfilename) and extension == "reascale":

            # ask if current treeview should be cleared before loading the file
            dialog = msgBox.askyesnocancel("Remove current items from treeview first?", "Clear current treeview widget first?\n\n'Yes' = Clear treeview first, 'No' = Append to treeview")
            if dialog == 1:
                self.clearView(self.getTabName(), False)

            try:
                with open(openfilename, "r") as f:
##                    msg(openfilename)
                    for line in f:
                        line.strip()

                        # lines with scales starts with 0
                        if line.startswith("0"):
                            scaleName = line.split()[1:-1]
                            for i, name in enumerate(scaleName):
                                if "'" in name:
                                    name = name.strip("'")
                                if '"' in name:
                                    name = name.strip('"')

                                scaleName[i] = name + " "


                            scaleName = "".join([char for char in scaleName])
                            scaleName = scaleName.strip()
                            scale = str(line.split()[-1])
                            scaleL = [char for char in scale]

                            for i, char in enumerate(scaleL):
                                if i > 0 and char != "0":
                                    pattern += str(i) + ", "
                                    patternLength += 1
                            pattern = pattern.rstrip(", ")

##                            a = pattern.split(",")
##                            for i in a:
##                                patternL.append(int(i.strip()))
##                            patternL = [int(x) for x in pattern.split(",")]
##                            print(patternL)

##                            # get "full scale" for pattern
##                            fullScale = self.makeFullScale(patternL)

##                            if self.getTabName() == "Patterns":
##                                print("sa")
##                                self.patternViewItemIdL.append(treeId)
##                                treeView.set(treeId, "All notes in selected pattern in selected root", fullScale)

                            treeId = self.patternview.insert("", 'end', text=scaleName)

                            self.patternViewItemIdL.append(treeId)
##                            self.patternview.set(treeId, "All notes in selected pattern in selected root", fullScale)
##                            self.patternViewItemIdL.append(treeId)
                            self.patternview.set(treeId, patternCol, pattern)
                            self.patternview.set(treeId, lengthCol, patternLength)

                            pattern = "0, "
                            patternLength = 1

##                self.lastSelected = ""

            except (IOError, PermissionError) as e:
                print(e)

    def clearView(self, viewName, showDialog):
        if showDialog and not msgBox.askyesno("Clear current treeview?", "Clear current treeview?"):
            return
        else:
            self.lastSelected = ""
            # clear pattern view
            if viewName == "Patterns":
                for item in self.patternViewItemIdL:
                    self.patternview.delete(item)
                self.patternViewItemIdL = []

            # clear chords view
            elif viewName == "Chords":
                for item in self.chordViewItemIdL:
                    self.chordview.delete(item)
                self.chordViewItemIdL = []

            # clear selector view
            elif viewName == "Selector":
                for item in self.selectionViewItemIdL:
                    self.selectionview.delete(item)
                self.selectionViewItemIdL = []

    def openPatternFile(self):
        if self.getTabName() == "Patterns":
            view = "patternView"
        elif self.getTabName() == "Chords":
            view = "chordView"
        elif self.getTabName() == "Selector":
            view = "selectionView"

        scriptPath = str(sys.path[0])

        openfilename=askopenfilename(initialdir=scriptPath, filetypes=[("pattern files", "*.txt")], title="Open a file containing scales (patterns)")
        extension = os.path.splitext(openfilename)[1][1:].strip().lower()

        if openfilename and os.path.isfile(openfilename) and extension == "txt":
        # ask if current treeview should be cleared before loading the file
            dialog = msgBox.askyesnocancel("Remove current items from treeview first?", "Clear current treeview widget first?\n\n'Yes' = Clear treeview first, 'No' = Append to treeview")
            if dialog == 1:
                self.clearView(self.getTabName(), False)
                self.populateView(view, openfilename)
                self.lastSelected = ""
            elif dialog == 0:
                self.populateView(view, openfilename)

##if __name__ == '__main__':
##    root = Tk()
##    app = Application(root)
##    root.mainloop()

@ProgramStartDirect
def Main():
    global root
##    root = tkinter.Tk()
    root = Tk()
    Application(root)
    root.mainloop()