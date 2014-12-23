from contextlib import contextmanager
from Chunkparser import *

@contextmanager
def undoable(message):
    RPR_Undo_BeginBlock2(0)
    try:
        yield
    finally:
        RPR_Undo_EndBlock2(0, message, -1)

with undoable("Remove CC events"):
    removeEvents("b")
