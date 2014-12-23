#This will change an FX parameter by "fxp" amount using OSC. It is linked to the Edit Cursor Position via a while loop.
#Note: You will note notice the FX param visually changing until end of script, but if you listen you will notice.

from reaper_python import * 

fxp = 0.0


CurPos = RPR_GetCursorPosition()
while CurPos < 5.0:
	RPR_MoveEditCursor(0.001,0)
	fxp = fxp + 0.0003
	RPR_OscLocalMessageToHost("/track/1/fx/1/fxparam/37/value", fxp)
	CurPos = RPR_GetCursorPosition()