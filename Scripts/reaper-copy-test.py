import os
import sys
from reaper_python import RPR_ShowConsoleMsg as log
path = os.path.join(sys.path[0], "script_data/myvars.txt")
log(path)