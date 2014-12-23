import beyond.Reaper
import beyond.Screen
from beyond.Reaper.Settings import *
import sys


@ProgramStart
class Main(Parallel):

	def Start(o):

		Say("beyond Python Version:", beyond.Version)
		Say()

		if Reaper_RemoteControl_CmdID == 123456:
			Say("beyond.Reaper is not Setup, check:", "/Modules/beyond/Reaper/Settings.py")
		else:

			Say("Connecting to Reaper:")
			Say("  RemoteControl.py Cmd ID:", Reaper_RemoteControl_CmdID)
			Say("  OSC Address:", Reaper_OSC_Address)
			Say("  External Program Address:", External_Program_Address)
			Say("  Python Executable:", Python)
			Say("  Python Executable (sys):", sys.executable)
			Say("  ...awaiting response:")

			with Reaper as r:
				Say("Connected!:")
				r.ShowConsoleMsg("Hello Reaper!\n")

			Say()
			Say("All Set!:")