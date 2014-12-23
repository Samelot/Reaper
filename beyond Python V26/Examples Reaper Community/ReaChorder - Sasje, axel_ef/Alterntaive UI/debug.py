# from reaper_python import *

debug = False

def msg(m):
    if (debug):
        Reaper.ShowConsoleMsg(str(m)+'\n')
    