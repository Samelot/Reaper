import beyond.Reaper
import beyond.Screen
from beyond.Reaper.Settings import *
import sys

import OSC
c = OSC.OSCClient()
c.connect(('127.0.0.1', 57120))   # connect to SuperCollider
oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/startup")
oscmsg.append('HELLO')
c.send(oscmsg)