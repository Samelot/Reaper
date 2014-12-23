import beyond.Reaper.Project
import beyond.Reaper.Effects
from beyond.Reaper.Elements import *


class Item(Proxy, beyond.Elements.Elements):
  
  def __Object__(c):
    o = c.Base()
    if c.New:
      o.HeaderElements = Elements()

  def Clear(o):
    super().Clear()
    o.HeaderElements.Clear()
    o.Elements.Clear()


  def Receive(o):
    S = Reaper.GetSetItemState(o.Address, "", o._ReceiveCapacity)[2]
    # Say(S)
    o.Elements = Elements(S).ITEM
    o.ReceiveElements()
    return o

  def Send(o):
    o.SendElements()
    S = o.Elements.Serial
    with Reaper as r:
      # r.PreventUIRefresh(1)
      r.Execute('L = RPR_GetSetItemState2(L[1], L[2], L[3], False)[0]', o.Address, S, len(S))
      # r.PreventUIRefresh(-1)  
    return o


  def ReceiveElements(o):

    super().Clear()
    o.HeaderElements.Clear()
    Target = o.HeaderElements
    if o.Connected:
      with Reaper as r:
        i = 0
        for E in o.Elements:
          if E.Name == "TAKE" or (Target is o.HeaderElements and E.Name == "NAME"):
            A = r.GetTake(o.Address, i)
            i += 1
            Target = o.Add(Take(A)).Elements
          Target.Add(E)
    else:
      for E in o.Elements:
        if E.Name == "TAKE" or (Target is o.HeaderElements and E.Name == "NAME"):
          Target = o.Add(Take()).Elements
        Target.Add(E)

    if len(o) > 0:
      AnyActive = False
      for T in o:
        if not T.Elements.Has("TAKE"): T.Elements.TAKE = WordBlank
        elif T.Elements.TAKE == "SEL": 
          AnyActive = True
          break
      if not AnyActive: o[0].Elements.TAKE = Word("SEL")
    
    return o


  def SendElements(o):

    o.Elements.Clear()

    for E in o.HeaderElements: o.Elements.Add(E)

    for T in o:
      # T.SendElements()
      for E in T.Elements: o.Elements.Add(E)

    if o.Elements.Has("TAKE"): del o.Elements.TAKE

    return o
  


  def ReceiveFile(o, File):
    S = File.Binary.decode("utf-8")
    o.Elements = Elements(S).ITEM
    o.ReceiveElements()
    return o

  def SendFile(o, File):
    o.SendElements()
    S = o.Elements.Serial
    File.Binary = S.encode("utf-8")
    return o






  _InfoGet = Reaper.GetMediaItemInfo_Value
  _InfoSet = Reaper.SetMediaItemInfo_Value

  @Property
  def Name(o, p):
    if p.Get: p.Value = o.TakeActive.Name
    elif p.Set: o.TakeActive.Name = p.Value
    

  @Property
  def Selected(o, p): 
    p.Value = o._GetSet("SEL", 0, "B_UISEL", False, p.Set, p.Value)
  
  @Property
  def TakeActive(o, p):
    if p.Get:
      if o.Connected:
        A = Reaper.GetActiveTake(o.Address)
        p.Value = Take(A)
      else:
        for T in o:
          if T.Elements.TAKE == "SEL": 
            p.Value = T
            break
    elif p.Set:
      Found = False
      for T in o:
        if p.Value is T and not Found:
          T.Elements.TAKE = Word("SEL")
          Found = True
        else:
          T.Elements.TAKE = WordBlank
      if Found:
        if o.Connected:
          with Reaper as r:
            r.SetActiveTake(p.Value.Address)
            r.MarkTrackItemsDirty(r.GetMediaItemTrack(o.Address), o.Address)
            r.UpdateItemInProject(o.Address)
      else:
        T = o.Add(p.Value.Copy())
        T.Address = None


Reaper.Item = Item

@Property
def ItemsSelected(o, p):
  with Reaper as r:
    for i in range(r.CountSelectedMediaItems(o.Address)):
      A = r.GetSelectedMediaItem(o.Address, i)
      yield Item(A)

Reaper.Project.ItemsSelected = ItemsSelected




class Take(Proxy, beyond.Elements.Element):

  def __Object__(c):
    o = c.Base()
    if c.New:
      o.Effects = Reaper.Effects()

  _InfoGet = Reaper.GetMediaItemTakeInfo_Value
  _InfoSet = Reaper.SetMediaItemTakeInfo_Value
  _InfoGetSetString = Reaper.GetSetMediaItemTakeInfo_String

  @Property
  def Name(o, p):
    p.Value = o._GetSet("NAME", 0, "P_NAME", "", p.Set, p.Value)
    if p.Set: p.Base()

  @Property
  def Active(o, p):
    if p.Get: p.Value = o == o.Container.TakeActive
    elif p.Set: o.Container.TakeActive = o