from beyond.Reaper.Elements import *


class Effects(beyond.Elements.Elements):
	
	def __Object__(c):
		o = c.Base()
		o.HeaderElements = Elements()
		o.Elements = Elements()


	def ReceiveElements(o):
		
		o.Clear()
		o.HeaderElements.Clear()

		Target = o.HeaderElements
		for E in o.Elements:

			if E.Name == "BYPASS":
				F = o.Add(Effect())
				Target = F.Elements
			Target.Add(E)

		for E in o:
			E.ReceiveElements()
	
	
	def SendElements(o):

		o.Elements.Clear()
	
		if len(o) > 0:
			
			for E in o.HeaderElements: o.Elements.Add(E)

			for F in o:
				F.SendElements()
				for E in F.Elements: o.Elements.Add(E)

		
Reaper.Effects = Effects



		
class Effect(beyond.Elements.Element):
	
	def __Object__(c):
		o = c.Base()
		o.Elements = Elements()
		o.Parameters = Parameters()
		o.PluginType = ""
		o.Plugin = ""


	def ReceiveElements(o):

		for E in o.Elements:
			if E.__class__ is Elements: 
				o.PluginType = E.Name
				break

		E = o.PluginElements
		o.Name = E[0][-1]
		o.Plugin = E[0][0]
		
		E = o.Elements
		o.Active = True if E.BYPASS[0] == 0 else False
		o.Online = True if E.BYPASS[1] == 0 else False
		
		if o.PluginType == "JS":
			o.Parameters.Clear()
			for E in o.Elements.JS[1]:
				if type(E) == float:
					P = o.Parameters.Add(Parameter())
					P.Value = E

	
	def SendElements(o):
		
		E = o.PluginElements
		E[0][-1] = o.Name
		E[0][0] = o.Plugin
		
		E = o.Elements
		E.BYPASS[0] = 0 if o.Active else 1
		E.BYPASS[1] = 0 if o.Online else 1

		if o.PluginType == "JS":
			E = o.Elements.JS[1]
			i = 0
			for P in o.Parameters:
				E[i] = P.Value
				i += 1

	
	@Property
	def PluginElements(o, p):
		p.Value = o.Elements.Get(o.PluginType)


		


class Parameters(beyond.Elements.Elements):
		
		
	def Receive(o, Names = False):
		
		T = o.Container.Container.Container.Address
		I = o.Container.Index
		
		o.Clear()

		L = Reaper.Execute("""
			
T, I, Names = L[1:]
N = ""
L = []

for P in range(RPR_TrackFX_GetNumParams(T, I) - 2):
	if Names: N = RPR_TrackFX_GetParamName(T, I, P, "", 128)[4]
	R = RPR_TrackFX_GetParamEx(T, I, P, 0, 0, 0)
	L.append((N, R[0], R[4], R[5], R[6]))
	
""", T, I, Names)
				
		for E in L:
			P = Parameter()
			P.Name, P.Value, P.Minimum, P.Maximum, P.Default = E
			o.Add(P)

		
		
	def Send(o):
		
		T = o.Container.Container.Container.Address
		I = o.Container.Index
		
		P = []
		for E in o: P.append(E.Value)

		Reaper.Execute("""
		
T, I, P = L[1:]
i = 0

for V in P: 
	RPR_TrackFX_SetParam(T, I, i, V)
	i += 1

L = []

""", T, I, P)
	
	
		
class Parameter(beyond.Elements.Element):
	pass
