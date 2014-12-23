import sys, io, time



class Stream(io.StringIO):

  def __iadd__(o, T):
    o.write(T)
    return o
  
  def Complete(o):
    T = o.getvalue()
    o.close()
    return T


    



SayOutputs = []


def SayFormat(*L):
  
  s = Stream()

  Seperator = ""
  
  for E in L: 
    
    s += Seperator
    
    C = E.__class__
    if C is str:
      if E.endswith(":"):
        s += E
        Seperator = " "
      else:
        s += '"'
        s += E
        s += '"'
        Seperator = ", "
    
    elif C is int or C is float or C is bool:
      s += str(E)
      Seperator = ", "
    
    elif hasattr(E, "Say") and E.Say != Say:
      Seperator = E.Say(s)
    
    elif isinstance(E, Exception):
      s += "\n== Exception ===========\n"
      T = getattr(E, "Traceback", None)
      if T is None:
        import traceback
        T = traceback.extract_tb(E.__traceback__)
      for File, LineNumber, Name, Line in T:
        s += '\nFile "'
        s += File
        s += '", line '
        s += str(LineNumber)
        s += ', in '
        s += Name
        s += '\n '
        s += str(Line)
        s += '\n'
      s += '\n'
      s += str(E)
      s += '\n'
        # Say('File "' + File + '", line ' + str(LineNumber) + ':')
        # Say(Name + '():', Line)
      s += "\n========================\n"
      Seperator = "\n"

    else:
      s += str(E)
      s += " ("
      s += C.__name__
      s += ")"
      Seperator = ", "
    
  s += "\n"
  
  return s.Complete()

  

@Omnipresent  
def Say_(*L):
  if sys.stdout is not None:
    sys.stdout.write(SayFormat(*L))
    sys.stdout.flush()


@Omnipresent  
def Say(*L):
  T = SayFormat(*L)
  if sys.stdout is not None:
    sys.stdout.write(T)
    sys.stdout.flush()
  for Output in SayOutputs: Output(T)


@Omnipresent  
def Saydir(o):
  for e in dir(o):
    Say(e + ":", getattr(o, e))




def ToNumber(T):
  try:
    if "." in T: return float(T)
    else: return int(T)
  except: return T
  

def SplitStart(T, Seperator):
  t = T.partition(Seperator)
  if t[1] == "" and t[2] == "": return "", T
  else: return t[0], t[2]

def SplitEnd(T, Seperator):
  t = T.rpartition(Seperator)
  if t[0] == "" and t[1] == "": return t[2], ""
  else: return t[0], t[2]

def Join(Start, Seperator, End):
  return Start if End == "" else Start + Seperator + End



@Omnipresent
def TimerStart(Name):
  global TimerStart_, TimerName
  TimerStart_ = time.clock()
  TimerName = Name

@Omnipresent  
def TimerEnd():
  Say(TimerName + ":", round(time.clock() - TimerStart_, 4))



  