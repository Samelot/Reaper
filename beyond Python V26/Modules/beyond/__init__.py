import sys, builtins

Version = 26

class Omnipresent():
  def __call__(o, E):
    setattr(builtins, E.__name__, E)
    return E
  def __getattribute__(o, Name): return getattr(builtins, Name)
  def __setattr__(o, Name, Value): setattr(builtins, Name, Value)
  def __delattr__(o, Name): delattr(builtins, Name)
builtins.Omnipresent = Omnipresent()
del Omnipresent


ImportOriginal = Omnipresent.__import__
def Import(name, globals = None, locals = None, fromlist = (), level = 0):
  R = ImportOriginal(name, globals, locals, fromlist, level)
  if name.startswith("beyond."):
    M = sys.modules[name]
    if hasattr(M, "_Import"): M._Import(M)
  return R
Omnipresent.__import__ = Import


@Omnipresent
def ProgramStartDirect(E):
  if E.__module__ == "__main__": E()
  else: return E


import beyond.Text