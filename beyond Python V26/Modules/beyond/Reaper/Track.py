import beyond.Reaper.Project
import beyond.Reaper.Effects
from beyond.Reaper.Elements import *




class Track(Proxy, beyond.Elements.Elements):


	def __Object__(c):
		o = c.Base()
		if c.New:
			o.Effects = Reaper.Effects()

			
	def Receive(o):
		S = Reaper.GetSetTrackState2(o.Address, "", o._ReceiveCapacity, False)[2]
		# Say("S:", S)
		o.Elements = Elements(S).TRACK
		o.ReceiveElements()
		return o

	def Send(o):
		
		o.Effects.HeaderElements.SHOW = 0
		
		for F in o.Effects:
			for E in F.Elements:
				if E.Name == "FLOAT": E.Name = "FLOATPOS"
		
		o.SendElements()
		S = o.Elements.Serial

		with Reaper as r:

			# Playing = r.GetPlayState() == 1
			# if Playing: r.OnStopButton()

			r.TrackFX_Show(o.Address, 0, 0)

			# for i in range(len(o.Effects)):
			# 	# Say(i)
			# 	# r.TrackFX_Show(o.Address, i, 0)
				# r.TrackFX_SetOpen(o.Address, i, False)
	
			# r.PreventUIRefresh(1)

			r.Execute('L = RPR_GetSetTrackState2(L[1], L[2], L[3], False)[0]', o.Address, S, len(S))
			
			# r.PreventUIRefresh(-1)

			# r.TrackFX_Show(o.Address, 0, 1)
			# r.TrackFX_Show(o.Address, 0, 0)

			# r.TrackFX_SetParam(o.Address, 0, 0, 0)

			# for i in range(len(o.Effects)):
			# 	# Say(i)
				# r.TrackFX_Show(o.Address, i, 3)
			# 	r.TrackFX_SetOpen(o.Address, i, False)

			# if Playing: r.OnPlayButton()




	def ReceiveElements(o):
		o.Effects.Clear()
		if o.Elements.Has("FXCHAIN"):
			o.Effects.Elements = o.Elements.FXCHAIN
			o.Effects.ReceiveElements()
		
	def SendElements(o):
		if len(o.Effects) == 0 and o.Elements.Has("FXCHAIN"):
			del o.Elements.FXCHAIN
		else:
			# Say(1, o.Elements.FXCHAIN, o.Effects.Elements)
			o.Elements.FXCHAIN = o.Effects.Elements
			# Say(2, o.Elements.FXCHAIN)
			o.Effects.SendElements()

	
	def ReceiveFile(o, File):
		# TimerStart("ReceiveFile")
		S = File.Binary.decode("utf-8")
		o.Elements = Elements(S).TRACK
		o.ReceiveElements()
		# TimerEnd()
		return o
		
	def SendFile(o, File):
		o.SendElements()
		S = o.Elements.Serial
		File.Binary = S.encode("utf-8")



			



	_InfoGet = Reaper.GetMediaTrackInfo_Value
	_InfoSet = Reaper.SetMediaTrackInfo_Value
	_InfoGetSetString = Reaper.GetSetMediaTrackInfo_String

	@Property
	def Selected(o, p): p.Value = o._GetSet("SEL", 0, "I_SELECTED", False, p.Set, p.Value)
	
	@Property
	def Name(o, p): p.Value = o._GetSet("NAME", 0, "P_NAME", "", p.Set, p.Value)

	@Property
	def FolderDelta(o, p): p.Value = o._GetSet("ISBUS", 1, "I_FOLDERDEPTH", 0, p.Set, p.Value)


Reaper.Track = Track




@Property
def Project_TracksSelected(o, p):
	with Reaper as r:
		
		T = o.TrackMaster
		if T.Selected: yield T

		for i in range(r.CountSelectedTracks(o.Address)):
			A = r.GetSelectedTrack(o.Address, i)
			yield Track(A)

Reaper.Project.TracksSelected = Project_TracksSelected


@Property
def Project_TrackMaster(o, p):
	p.Value = Track(Reaper.GetMasterTrack(o.Address))

Reaper.Project.TrackMaster = Project_TrackMaster


@Property
def Project_TracksAll(o, p):
	with Reaper as r:
	  for i in range(r.CountTracks(o.Address)):
	    A = r.GetTrack(o.Address, i)
	    yield Track(A)

Reaper.Project.TracksAll = Project_TracksAll


def Project_Receive(o):
  Target = o
  Target.Clear()
  for T in o.TracksAll:
    Target.Add(T)
    d = T.FolderDelta
    if d == 1:
    	Target = T
    	Target.Clear()
    elif d < 0:
      for c in range(-d): Target = Target.Container

def Project_Receive2(o):
  
  L = Reaper.Execute("""
P = L[1]
L = []
for i in range(RPR_CountTracks(P)):
  T = RPR_GetTrack(P, i)
  d = int(RPR_GetMediaTrackInfo_Value(T, "I_FOLDERDEPTH"))
  L.append((T, d))
  """, o.Address)

  Target = o
  Target.Clear() 
  for T, d in L:
    T = Track(T)
    Target.Add(T)
    if d == 1:
    	Target = T
    	Target.Clear()
    elif d < 0:
      for c in range(-d): Target = Target.Container

Reaper.Project.Receive = Project_Receive2