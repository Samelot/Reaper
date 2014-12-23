from tkinter import *
from tkinter import ttk

import argparse

##from pythonosc import osc_message_builder
##from pythonosc import udp_client

import osc_message_builder
import udp_client

##from pythonosc import osc_bundle_builder

# get these values from REAPER Preferences -> Control Surfaces:
hostIP = "10.0.0.4" # Host IP
port = 8000 # Messages are sent to this port -> REAPER receives on this port

class OSCClient:

    def __init__(self, root):
        self.root = root
        self.root.wm_attributes("-topmost", 1)  # for Mac users: remove or "comment out" this line
        self.root.grid_columnconfigure(0, weight=1)
##        self.root.grid_rowconfigure(0, weight=1)

        self.makeWidgets()

    def makeWidgets(self):
        # parent frame for main container frames (parent = self.root)
        self.frParent = ttk.Frame(self.root)

        # put container frames to parent frame:
        # container frame "top" (parent = self.frParent)
        self.frContainerTop = ttk.Frame(self.frParent)

        # container frame "middle" (parent = self.frParent)
        self.frContainerMiddle = ttk.Frame(self.frParent)

        # container frame "bottom" (parent = self.frParent)
        self.frContainerBottom = ttk.Frame(self.frParent)

        # put sliders, buttons and edit boxes to separate container frames
        # container frames + entries "IP/port"
        self.frEBoxHostIP = ttk.Labelframe( self.frContainerTop, text="Send to IP (REAPER):")
        self.frEBoxPortIP = ttk.Labelframe( self.frContainerTop, text="Send to Port (REAPER):")

        # set IP address to StringVar
        self.sHostIP = StringVar()
        self.sHostIP.set(hostIP)

        # set port number to StringVar
        self.sHostPort = StringVar()
        self.sHostPort.set(port)

        # edit box "Send to IP"
        self.eBoxHostIP = ttk.Entry(        self.frEBoxHostIP,
                                            textvariable=self.sHostIP,
                                            state = DISABLED)
        # edit box "Send to Port"
        self.eBoxHostPort = ttk.Entry(      self.frEBoxPortIP,
                                            textvariable=self.sHostPort,
                                            state = DISABLED)


        # volume slider values
        # values are converted to 0...1, step = 0.001 in setVolume() function
        self.sliderVolRangeB = 0
        self.sliderVolRangeU = 1000
        self.sliderVolDefVal = 600  # 0 db
##        self.sliderVolVal = DoubleVar()
        self.sliderVolVal = IntVar()    # this variable contains the slider value (0 to 1000)
        self.sliderVolVal.set(self.sliderVolDefVal)

        # container frame + volume slider + buttons (Track 1)
        self.frTrack1 = ttk.Labelframe( self.frContainerMiddle, text="Track 1")
        self.sliderVolume1 = ttk.Scale( self.frTrack1,
                                        from_= self.sliderVolRangeB,
                                        to = self.sliderVolRangeU,
##                                        value = self.sliderVolDefVal,   # default value
                                        command = self.setVolume,       # this function is called when slider is moving
                                        variable = self.sliderVolVal)   # contains slider's (current) value

        self.btnMute1 = ttk.Button(     self.frTrack1,
                                        text = "M",
                                        command = lambda: self.mute(1),   # mute Track 1
                                        width = 1)

##        self.valSliderVol = DoubleVar()
##        self.lblSliderVol1 = ttk.Label( self.frTrack1,
##                                        text = "M",
##                                        textvariable = self.valSliderVol,
##                                        width = 2)


        # container frame + play button
        self.frBtnPlay = ttk.Frame(     self.frContainerMiddle)
        self.btnPlay = ttk.Button(      self.frBtnPlay,
                                        command = self.play,
                                        text = "Play/Pause")

        # container frame + stop button
        self.frBtnStop = ttk.Frame(     self.frContainerMiddle)
        self.btnStop = ttk.Button(      self.frBtnStop,
                                        command = self.stop,
                                        text = "Stop")

        # container frame + record button
        self.frBtnRecord = ttk.Frame(   self.frContainerMiddle)
        self.btnRecord = ttk.Button(    self.frBtnRecord,
                                        command = self.record,
                                        text = "Record")

        self.placeWidgetsToGrid()

    def placeWidgetsToGrid(self):
        # parent frame (placed to root)
        self.frParent.grid(             sticky=(N,W,E,S),   row=0, column=0)
        self.frParent.grid_columnconfigure(0, weight=1)

        # main container frames (placed to parent frame)
        self.frContainerTop.grid(       sticky=(N,W,E,S),   row=0, column=0)
        self.frContainerMiddle.grid(    sticky=(N,W,E,S),   row=1, column=0)
        self.frContainerMiddle.grid_columnconfigure(0, weight=1)
        self.frContainerBottom.grid(    sticky=(N,W,E,S),   row=3, column=0)

        # container frames for buttons/sliders (placed to main container frames)
        # entry "Host IP" (placed to "Top" frame)
        self.frEBoxHostIP.grid(         sticky=(N,W,E,S),   row=0, column=0)
        self.eBoxHostIP.grid(           sticky=(N,W,E,S),   row=0, column=0)

        # entry "Host Port" (placed to "Top" frame)
        self.frEBoxPortIP.grid(         sticky=(N,W,E,S),   row=0, column=1)
        self.eBoxHostPort.grid(         sticky=(N,W,E,S),   row=0, column=0)

        # "track" label frame (placed to "Middle" frame)
        self.frTrack1.grid(             sticky=(N,W,E,S),   row=1, column=0,
                                        columnspan = 2)
        self.frTrack1.grid_columnconfigure(0, weight=1)

        # slider + mute button (placed to track label frame)
        self.sliderVolume1.grid(        sticky=(N,W,E,S),   row=2, column=0)
        self.btnMute1.grid(             sticky=(W),         row=0, column=0)
##        self.lblSliderVol1.grid(        sticky=(W,E),       row=1, column=0,
##                                        columnspan = 2)
        # container frames for play/stop/rec -buttons
        # these are placed to "Bottom" frame
        self.frBtnPlay.grid(            sticky=(N,W,E,S),   row=2, column=0)
        self.frBtnStop.grid(            sticky=(N,W,E,S),   row=3, column=0)
        self.frBtnRecord.grid(          sticky=(N,W,E,S),   row=4, column=0)

        # play/stop/record buttons (placed to container frames above)
        self.btnPlay.grid(              sticky=(N,W,S),     row=0, column=0)
        self.btnStop.grid(              sticky=(N,W,S),     row=0, column=0)
        self.btnRecord.grid(            sticky=(N,W,S),     row=0, column=0)

        self.widgetBindings()

    def widgetBindings(self):
##        # left mouse btn up -> move slider to default position:
##        self.sliderVolume1.bind("<ButtonRelease-1>", lambda event: (self.sliderVolVal.set(self.sliderVolDefVal), self.setVolume(event)))
        # double left mouse btn -> move slider to default position:
        self.sliderVolume1.bind("<Double-Button-1>", lambda event: (self.sliderVolVal.set(self.sliderVolDefVal), self.setVolume(event)))
        self.initOscClient()

# init Client

    def initOscClient(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=hostIP,
                            help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=port,
                            help="The port the OSC server is listening on")
        args = parser.parse_args()
        self.client = udp_client.UDPClient(args.ip, args.port)

# GUI functions

    def setVolume(self, event):
        sliderVal = float(self.sliderVolVal.get())

        # convert range: "0 -> 1000" to "0 -> 1" (step = 0.001)
        sliderVal = sliderVal / 1000

        msg = osc_message_builder.OscMessageBuilder(address = "/track/1/volume")
        msg.add_arg(sliderVal)
##        print(msg.args)
        self.sendOSCdata(msg)
##        self.valSliderVol.set(sliderVal)

    def play(self):
        msg = osc_message_builder.OscMessageBuilder(address ="/play")
        self.sendOSCdata(msg)

    def stop(self):
        msg = osc_message_builder.OscMessageBuilder(address ="/stop")
        self.sendOSCdata(msg)

    def record(self):
        msg = osc_message_builder.OscMessageBuilder(address ="/record")
        self.sendOSCdata(msg)

    def mute(self, trackIndex):
        msg = osc_message_builder.OscMessageBuilder(address ="/track/" + str(trackIndex) + "/mute")
##        msg.add_arg(1, osc_message_builder.OscMessageBuilder.ARG_TYPE_INT)
        msg.add_arg(1)
        self.sendOSCdata(msg)

    def sendOSCdata(self, msg):
        msg = msg.build()
##        print(msg.address)
        self.client.send(msg)

if __name__ == '__main__':
    root = Tk()
    app = OSCClient(root)
    root.mainloop()