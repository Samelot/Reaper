from tkinter import *
from tkinter import ttk
import beyond.Reaper


class Application:

    trackIdList = []
    trackNameList = []
    treeTrackIdList = []
    treeItemIdList = []
    itemPos = []

    def __init__(self, root):
        self.root = root
        self.root.wm_attributes("-topmost", 1)
    ##        self.root.attributes("-toolwindow", 1)
        self.root.geometry('300x400+0+0')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.makeWidgets()

    def makeWidgets(self):
        # treeview widget
        # set displaycolumns=["idColumn","PosColumn"] to show Id and Position -columns
        self.tree = ttk.Treeview(self.root, columns=["idColumn","PosColumn"], displaycolumns=[] ,selectmode="browse", show="tree headings")
        self.tree.column("#0", width=200)
        self.tree.heading("idColumn", text="Id")
        self.tree.heading("PosColumn", text="Position")
        self.tree.heading("#0", text="Name", command = self.headingClicked)

        self.tree.tag_bind('tracks', '<Control-Button-1>', self.trackCtrlMouseL)
        self.tree.tag_bind('items', '<Control-Button-1>', self.itemCtrlMouseL)
        self.tree.tag_bind('items', '<Shift-Button-1>', self.itemShiftMouseL)
        self.tree.tag_bind('takes', '<Control-Button-1>', self.takeCtrlMouseL)

        self.tree.tag_configure('tracks', background='#f0f0f0')
        self.tree.tag_configure('items', background='#f0f0ff')
        self.tree.tag_configure('takes', background='#f0faff')

        self.tree.bind('<<TreeviewSelect>>', self.treeSelected)
        self.tree.grid(column=0, row=0, columnspan = 2, sticky=(N,W,E,S))

        # scrollbar for treeview
        self.sb = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.sb.grid(column=2, row=0, sticky=(N,S))
        self.tree['yscrollcommand'] = self.sb.set

        # information label
        # info value is updated in function itemSelected() when selection changes
        self.info = StringVar()
        self.infolabel = ttk.Label(self.root, textvariable=self.info)
        self.infolabel.grid(column=0, row=1, columnspan = 2, sticky=(W,E))
        self.info.set("Press 'Refresh' to update")

        # Refresh button
        self.button1 = ttk.Button(self.root, text="Refresh", command=self.populate)
        self.button1.grid(column=0, row=2, sticky=(E))

        # Play button
        self.button1 = ttk.Button(self.root, text="Play", command=self.play)
        self.button1.grid(column=1, row=2, sticky=(W))

        # popup menu
        self.rClickMenu = Menu(self.root, tearoff=0)
        self.rClickMenu.add_command(label="Expand tracks", command=self.expandTracks)
        self.rClickMenu.add_command(label="Collapse tracks", command=self.collapseTracks)
        self.rClickMenu.add_command(label="Expand items", command=self.expandItems)
        self.rClickMenu.add_command(label="Collapse items", command=self.collapseItems)

        self.tree.bind("<Button-3>", self.popup)

    # right click selects items too
    def popup(self, event):
        itemUnderMcursor = self.tree.identify_row(event.y)
        self.tree.selection_set(itemUnderMcursor)
        # show popup menu at mouse cursor
        self.rClickMenu.post(event.x_root, event.y_root)

    def populate(self):
        # clear all first
        self.trackIdList = []
        self.trackNameList = []
        self.treeTrackIdList = []
        self.treeItemIdList = []
        self.itemPos = []
        self.info.set("Getting tracks...")   # add text to infolabel
        self.tree.update_idletasks()
        rootChildren = self.tree.get_children()
        for item in rootChildren:
            self.tree.delete(item)

        with Reaper as r:
            # get track ids and names
            trackCount = r.CountTracks(0)
            if trackCount == 0:
                self.info.set("No tracks")
                return
            for i in range(trackCount):
                trackPointer = r.GetTrack(0, i)
                trkNumber = int(r.GetMediaTrackInfo_Value(trackPointer, "IP_TRACKNUMBER"))
                trackName = r.GetTrackState(trackPointer, 0)[0]
                self.trackIdList.append(trackPointer)
                self.trackNameList.append(trackName)
                # add track name to tree
                treeTrackId = self.tree.insert('', 'end', text=str(trkNumber) + " " + trackName , tags='tracks')
                # add track pointer to hidden column
                self.tree.set(treeTrackId, "idColumn", trackPointer)
                self.treeTrackIdList.append(treeTrackId)

                # get item ids and positions
                mediaItemNum = r.CountTrackMediaItems(trackPointer)
                for itemIdx in range(mediaItemNum):
                    mediaItem = r.GetTrackMediaItem(trackPointer, itemIdx)
                    textVar = "item " + str(itemIdx + 1) + "/" + str(mediaItemNum)
                    # add current item to (parent)track
                    treeItemId = self.tree.insert(treeTrackId, 'end', text=textVar , tags='items')
                    self.tree.set(treeItemId, "idColumn", mediaItem)
                    self.treeItemIdList.append(treeItemId)
                    # get position and add it to the hidden Position column
                    mediaItemPos = r.GetMediaItemInfo_Value(mediaItem,"D_POSITION")
                    self.tree.set(treeItemId, "PosColumn", mediaItemPos)
                    self.itemPos.append(mediaItemPos)

                    # get take ids and names
                    takeNum = r.CountTakes(mediaItem)
                    for takeIdx in range(takeNum):
                        take = r.GetTake(mediaItem, takeIdx)
                        takeName = r.GetSetMediaItemTakeInfo_String(take, "P_NAME", "", 0)[3]
                        if takeName == " ":
                            takeName = "<No Name>"
                        # add current take to (parent)item
                        treeTakeID = self.tree.insert(treeItemId, 'end', text=str(takeIdx + 1) + "/" + str(takeNum) + " " + takeName, tags='takes')
                        self.tree.set(treeTakeID, "idColumn", take)

            self.info.set("")   # add text to infolabel
            self.tree.selection_set(self.treeTrackIdList[0]) # set first treeitem selected

    def play(self):
        with Reaper as r:
            r.Main_OnCommand(40044, 0) # Play/stop

    def treeSelected(self, event):
        if self.trackIdList != []:  # check if there are tracks in treeview
            sel = self.tree.selection()[0] # get id from selected treeitem
            itemText = self.tree.item(sel, "text")   # get text from selected treeitem
            self.info.set(itemText)   # add text to infolabel

    def expandTracks(self):
        sel = self.tree.selection()[0] # get id from selected treeitem
        for i in self.treeTrackIdList:
            self.tree.item(i, open=True)    # expand every parent item
        self.tree.update_idletasks()
        self.tree.see(sel) # show focused item (scroll if necessary)

    def collapseTracks(self):
        sel = self.tree.selection()[0] # get id from selected treeitem
        for i in self.treeItemIdList:
            self.tree.item(i, open=False)
        for i in self.treeTrackIdList:
            self.tree.item(i, open=False)
        self.tree.see(sel)

    def expandItems(self):
        sel = self.tree.selection()[0] # get id from selected treeitem
        for i in self.treeTrackIdList:
            self.tree.item(i, open=True)    # expand every parent item
        for i in self.treeItemIdList:
            self.tree.item(i, open=True)
        self.tree.update_idletasks()
        self.tree.see(sel)

    def collapseItems(self):
        sel = self.tree.selection()[0] # get id from selected treeitem
        for i in self.treeItemIdList:
            self.tree.item(i, open=False)
        self.tree.see(sel)

    def headingClicked(self):
        pass

    def trackCtrlMouseL(self, event):
        pass

    # move edit cursor to start of item
    def itemCtrlMouseL(self, event):
        self.info.set("Moving edit cursor...")
        self.tree.update_idletasks()
        itemUnderMcursor = self.tree.identify_row(event.y)
        self.tree.selection_set(itemUnderMcursor)
        pos = self.tree.item(itemUnderMcursor, "value")[1] # pos[1] is position
        with Reaper as r:
            r.SetEditCurPos2(0,pos, 1, 1)

    def itemShiftMouseL(self, event):
        self.info.set("Selecting item...")
        self.tree.update_idletasks()
        itemUnderMcursor = self.tree.identify_row(event.y)
        self.tree.selection_set(itemUnderMcursor)
        pointer = self.tree.item(itemUnderMcursor, "value")[0] # pointer[0] is trackpointer
        with Reaper as r:
            r.Main_OnCommand(40769, 0)  # Unselect all tracks/items/envelopepoints
            r.SetMediaItemInfo_Value(pointer, "B_UISEL", 1) # set item selected
            r.UpdateItemInProject(pointer)
    ##        self.itemCtrlMouseL(event)

    def takeCtrlMouseL(self, event):
        pass


@ProgramStartDirect
def Main():
    root = Tk()
    app = Application(root)
    root.mainloop()