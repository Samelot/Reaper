import beyond
import sys


MainModule = sys.modules["__main__"]
RunningInside = hasattr(MainModule, "obj")



if RunningInside:


  SayOutputClear = False

  def SayOutput(Text):
    global SayOutputClear
    if not SayOutputClear:
      MainModule.RPR_ShowConsoleMsg("")
      SayOutputClear = True
    MainModule.RPR_ShowConsoleMsg(Text)

  beyond.Text.SayOutputs.append(SayOutput)



  ModuleClass = type(beyond)
  Omnipresent.ReaperImportOriginal = Omnipresent.__import__
  def Import(name, globals = None, locals = None, fromlist = (), level = 0):
    if name.startswith("beyond"):
      return ModuleClass(name)
    else:
      return ReaperImportOriginal(name, globals, locals, fromlist, level)
  Omnipresent.__import__ = Import

  @Omnipresent
  def ProgramStart(E):

    Omnipresent.__import__ = ReaperImportOriginal
    import os.path, subprocess, beyond.Reaper.Settings
  
    P = sys.path[0]
    P = os.path.normpath(P)
    F = MainModule.obj.co_filename
    F = os.path.join(P, F)

    if not os.path.isfile(Settings.Python):
      Say("Cannot find Python:", Settings.Python)

    if not os.path.isfile(F):
      Say("Cannot find Program:", F)

    subprocess.Popen([Settings.Python, F])

  Omnipresent.ProgramStartDirect = ProgramStart
  Omnipresent.Parallel = object
  Omnipresent.Screen = object



else:


  import socket, struct

  def SendOSC_Action(Address, ActionID):
    S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    S.sendto(struct.pack(">12si", b"/action\0,i\0\0", ActionID), Address)
    S.close()

  
  import beyond.Class
  import beyond.Network
  import beyond.Reaper.Settings

  class Reaper(Class):

    __PropertiesNative__ = "Depth", "Server", "Execute", "OnConnectExecute", "OnDisconnectHandlers"

    def __Object__(c):
      o = c.Base()
      o.Depth = 0
      o.OnConnectExecute = None
      o.OnDisconnectHandlers = set()

    def __enter__(o):
      if o.Depth == 0:
        # Say("REAPER Start:")
        try:
          SendOSC_Action(Settings.Reaper_OSC_Address, Settings.Reaper_RemoteControl_CmdID)
          o.Server = beyond.Network.ServerSingle(Settings.External_Program_Address)
        except Exception as E:
          Say()
          Say("Cannot Connect to Reaper:") 
          Say("Is Reaper running and /Modules/beyond/Reaper/Settings.py correct?:")
          Say("  Reaper_RemoteControl_CmdID:", Settings.Reaper_RemoteControl_CmdID)
          Say("  Reaper_OSC_Address:", Settings.Reaper_OSC_Address)
          Say()
          raise E
      o.Depth += 1
      if o.OnConnectExecute is not None:
        try: o.Execute(o.OnConnectExecute)
        except: pass
      return o

    def __exit__(o, ExceptionType, Exception, Traceback):
      o.Depth -= 1
      if o.Depth == 0 or Exception is not None:
        # Say("REAPER End:")

        o.Depth = 1
        for H in o.OnDisconnectHandlers:
          try: H._ReaperDisconnect()
          except: pass
        o.Depth = 0

        try:
          o.Server.Send(('Active = False',))
        except: pass
        o.Server.End()

    def Execute(o, *L):
      if o.Depth == 0:
        with o:
          o.Server.Send(L)
          R = o.Server.Receive()
      else:
        o.Server.Send(L)
        R = o.Server.Receive()
      if isinstance(R, Exception):
        Say("\nFrom Reaper:", R)
        raise Exception("Reaper Exception: " + str(R))
      return R

    def __PropertiesDynamic__(o, p):
      p.Base()
      if p.Get and not p.Exists:
        P, N = beyond.Text.SplitStart(p.Name, "_")
        if P.isupper(): N = p.Name
        else: N = "RPR_" + p.Name
        C = 'L = ' + N + '(*L[1:])'
        p.Value = lambda *L: o.Execute(C, *L)
        p.Exists = True

  Omnipresent.Reaper = Reaper()



  # import weakref
  Proxies = {}#weakref.WeakValueDictionary()

  class Proxy(Class):

    __PropertiesNative__ = "Address"

    def __Object__(c, Address = None):
      if Address is not None:
        c.Object = Proxies.get(Address, None)
        c.New = False
      if c.Object is None:
        o = c.Base()
        o.Address = Address
        Proxies[Address] = o
        c.New = True
