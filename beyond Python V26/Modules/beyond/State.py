# import beyond
import beyond.File
import io, pickle



class State:

	def Apply(o, Target):

		D = {}
		
		for E, V in o.Elements.items():
			if V.__class__ is State and hasattr(Target, E): 
				V.Apply(getattr(Target, E))
			else:
				D[E] = V
		
		Target.StateSet(D)

def _Import(o):
	State.__module__ = "beyond"
	beyond.State = State


class Statable:

	def __reduce__(o):
		F = o.StateGet
		if hasattr(F, "Parallel"): E = F(WaitReturn = True)
		else: E = F()
		return State, (), {"ClassName": o.__class__.__name__, "Elements": E}

		
	def StateGet(o):
		return o.__dict__
		
	def StateSet(o, D):
		o.__dict__.update(D)
		
	def StateSave(o, Stream):
		if type(Stream) is File:
			Stream = open(Stream.Path, "wb")
			pickle.dump(o, Stream, pickle.HIGHEST_PROTOCOL)
			Stream.close()
		else:
			pickle.dump(o, Stream, pickle.HIGHEST_PROTOCOL)

	def StateLoad(o, Stream):
		if type(Stream) is File:
			Stream = open(Stream.Path, "rb")
			S = pickle.load(Stream)
			Stream.close()
		else:
			S = pickle.load(Stream)
		S.Apply(o)

beyond.Statable = Statable