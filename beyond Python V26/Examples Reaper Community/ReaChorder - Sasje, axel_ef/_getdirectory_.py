import sys
import os

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        if sys.hexversion < 0x03000000: 
            return os.path.dirname(unicode(sys.executable, encoding))
        else:
            return os.path.dirname(str(sys.executable, encoding))
    if sys.hexversion < 0x03000000: 
        return os.path.dirname(unicode(__file__, encoding))
    else:
        return os.path.dirname(__file__)


class Test:
    autoComplete = 1
    