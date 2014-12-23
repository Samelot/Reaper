import beyond
import types



class MetaClass(type):

  def __new__(Class, Name , Bases, Dictionary):
    # Say(Name, Bases)

    if "__PropertiesDynamic__" in Dictionary:
      Found = False
      for C in Bases: 
        if hasattr(C, "__PropertiesDynamic__"): 
          Found = True
          break
      if not Found:
        Bases = list(Bases)
        Bases.insert(0, PropertiesDynamic)
        Bases = tuple(Bases)

    P = _PropertiesNativeGet(Dictionary)
    for C in Bases: P |= _PropertiesNativeGet(C.__dict__)
    if len(P) > 0: Dictionary["__PropertiesNative__"] = P

    Class = super().__new__(Class, Name, Bases, Dictionary)
    return Class


  def __call__(Class, *L, **D):
    c = ObjectConstructor()
    c.Object = None
    c.ClassChain = Class.mro()
    c.ClassIndex = 0
    c.ParameterList = L
    c.ParameterDictionary = D
    return c.Base()



def _PropertiesNativeGet(D):
  P = D.get("__PropertiesNative__", None)
  if P is None: P = ()
  elif type(P) is str: P = (P,)
  P = set(P)
  return P



class ObjectConstructor():

  def BaseFirst(c):
    Class = c.ClassChain[0]
    I = Class.__init__
    if I is object.__init__ or I.__code__.co_argcount == 1:
      c.Object = type.__call__(Class)
    else:
      c.Object = type.__call__(Class, *c.ParameterList, **c.ParameterDictionary)
    return c.Object

  def Base(c):
    while c.ClassIndex <= len(c.ClassChain):
      Class = c.ClassChain[c.ClassIndex]
      c.ClassIndex += 1
      E = Class.__dict__.get("__Object__", None)
      if E is not None:
        # Say("__Object__:", Class.__name__, Class.__module__)
        if E.__code__.co_argcount == 1:
          E(c)
        else:
          E(c, *c.ParameterList, **c.ParameterDictionary)
        return c.Object


@Omnipresent
class Class(metaclass = MetaClass):
  def __Object__(c):
    c.BaseFirst()



@Omnipresent
class Property(property):
  
  def __init__(o, Function):

    o.Function = Function

    def Get(o):
      p = PropertyAccess()
      p.Object = o
      p.ClassChain = type(o).mro()
      p.ClassIndex = 0
      p.ClassSearch = True
      p.Name = Function.__name__
      p.Get = True
      p.Set = False
      p.Delete = False
      p.Exists = True
      p.Value = None
      p.Base()
      if not p.Exists: raise AttributeError(str(p) + ": Does not exist")
      return p.Value
    
    def Set(o, Value):
      p = PropertyAccess()
      p.Object = o
      p.ClassChain = type(o).mro()
      p.ClassIndex = 0
      p.ClassSearch = True
      p.Name = Function.__name__
      p.Get = False
      p.Set = True
      p.Delete = False
      p.Exists = True
      p.Value = Value
      p.Base()
      if not p.Exists: raise AttributeError(str(p) + ": Does not exist")

    def Delete(o):
      p = PropertyAccess()
      p.Object = o
      p.ClassChain = type(o).mro()
      p.ClassIndex = 0
      p.ClassSearch = True
      p.Name = Function.__name__
      p.Get = False
      p.Set = False
      p.Delete = True
      p.Exists = True
      p.Value = None
      p.Base()
      if not p.Exists: raise AttributeError(str(p) + ": Does not exist")

    super().__init__(Get, Set, Delete)



class PropertiesDynamic():

  __PropertiesNative__ = set()

  def __getattribute__(o, Name):
    C = type(o)
    if Name.startswith("__") or Name in C.__PropertiesNative__: return super().__getattribute__(Name)
    else:
      p = PropertyAccess()
      p.Object = o
      p.ClassChain = C.mro()
      p.ClassIndex = 0
      p.ClassSearch = True
      p.Name = Name
      p.Get = True
      p.Set = False
      p.Delete = False
      p.Exists = True
      p.Value = None
      p.Base()
      if not p.Exists: raise AttributeError(str(p) + ": Does not exist")
      return p.Value

  def __setattr__(o, Name, Value):
    C = type(o)
    if Name.startswith("__") or Name in C.__PropertiesNative__: super().__setattr__(Name, Value)
    else:
      p = PropertyAccess()
      p.Object = o
      p.ClassChain = C.mro()
      p.ClassIndex = 0
      p.ClassSearch = True
      p.Name = Name
      p.Get = False
      p.Set = True
      p.Delete = False
      p.Exists = True
      p.Value = Value
      p.Base()
      if not p.Exists: raise AttributeError(str(p) + ": Does not exist")

  def __delattr__(o, Name):
    C = type(o)
    if Name.startswith("__") or Name in C.__PropertiesNative__: super().__delattr__(Name)
    else:
      p = PropertyAccess()
      p.Object = o
      p.ClassChain = C.mro()
      p.ClassIndex = 0
      p.ClassSearch = True
      p.Name = Name
      p.Get = False
      p.Set = False
      p.Delete = True
      p.Exists = True
      p.Value = None
      p.Base()
      if not p.Exists: raise AttributeError(str(p) + ": Does not exist")



class PropertyAccess:

  def BaseFirst(p):
    try:
      if p.Get: p.Value = p.Object.__dict__[p.Name]
      elif p.Set: p.Object.__dict__[p.Name] = p.Value
      elif p.Delete: del p.Object.__dict__[p.Name]
      p.Exists = True
    except KeyError:
      p.Exists = False  


  def Base(p):

    while p.ClassIndex <= len(p.ClassChain):

      if p.ClassIndex == len(p.ClassChain): p.BaseFirst()
      else:

        C = p.ClassChain[p.ClassIndex]

        if p.ClassSearch:
          E = C.__dict__.get(p.Name, None)
          if E is not None:
            p.ClassSearch = False
            if type(E) is Property:
              # Say(C.__name__ + " Property:")
              R = E.Function(p.Object, p)
              if type(R) is types.GeneratorType: p.Value = R
            elif type(E) is types.FunctionType:
              p.Value = types.MethodType(E, p.Object)
            else:
              p.Value = E
            break

        E = C.__dict__.get("__PropertiesDynamic__", None)
        if E is not None:
          p.ClassIndex += 1
          p.ClassSearch = True
          # Say(C.__name__ + " PropertiesDynamic:")
          R = E(p.Object, p)
          if type(R) is types.GeneratorType: p.Value = R
          break

      p.ClassIndex += 1
      p.ClassSearch = True


  def BaseGet(p, Name = None):
    p2 = PropertyAccess()
    p2.Object = p.Object
    p2.ClassChain = p.ClassChain
    p2.ClassIndex = p.ClassIndex
    p2.ClassSearch = p.ClassSearch
    p2.Name = p.Name if Name is None else Name
    p2.Get = True
    p2.Set = False
    p2.Delete = False
    p2.Exists = True
    p2.Value = None
    p2.Base()
    return p2


  def SameAs(p, Name):
    p.Name = Name
    getattr(type(p.Object), Name).Function(p.Object, p)


  def __str__(p):
    s = "Property "
    if p.Get: s += "Get"
    elif p.Set: s += "Set"
    elif p.Delete: s += "Delete"
    s += ' "' + p.Name + '"'
    return s