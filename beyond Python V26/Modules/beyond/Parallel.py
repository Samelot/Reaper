import beyond
import beyond.State
import threading, queue, time, types, sys



Parallels = {}
ParallelsLock = threading.Lock()


@Omnipresent
class Parallel(beyond.Statable):


	def __init__(o, Parent = None, Stay = False, **D):
				
		o.__dict__["Parent"] = Parent
		o.__dict__.update(D)
						
		o.Queue = queue.Queue()
		o.Active = True

		o.Thread = T = Parallel.Thread()
		T.name = o.__class__.__name__
		T.Parallel = o
		
		with ParallelsLock: Parallels[T] = o
		
		o.Start()
		T.start()
		if not Stay: o.End()
			

	class Thread(threading.Thread):
		def	run(o):
			o = o.Parallel
			while o.Active: o.Yield()
			with ParallelsLock: del Parallels[o.Thread]
			# Say_("Parallel Exit:", o.Thread.name)
		
	
	def Yield(o, Duration = None):
		if Duration is not None: WaitEnd = time.clock() + Duration
		while True:
			Now = time.clock()
			if not o.Active or (Duration is not None and Now >= WaitEnd):
				break
			elif not o.Queue.empty():
				L, D = o.Queue.get()
				Execute(*L, **D)
			else:
				time.sleep(0.001)

				
	def End(o):
		if o.Active:
			o.Active = False
			o.Free()

	def Execute(__o__, *L, **D):
		if __o__.Thread is threading.currentThread():
			Execute(*L, **D)
		else:
			__o__.Queue.put((L, D))
		
	def ExecuteWaitReturn(__o__, ___Function___, *L, **D):
		# Say_("ExecuteWaitReturn:", ___Function___)
		if __o__.Thread is threading.currentThread():
			return ___Function___(*L, **D)
		else:
			Ready = threading.Event()
			Return = []
			# __o__.Queue.put((('Return.append(Function(*L, **D))\nReady.set()',), {"Return": Return, "Ready": Ready, "Function": ___Function___, "L": L, "D": D}))
			__o__.Execute('Return.append(Function(*L, **D))\nReady.set()', Return = Return, Ready = Ready, Function = ___Function___, L = L, D = D)
			while not Ready.isSet() and __o__.Active: Ready.wait(.01)
			return Return[0] if len(Return) == 1 else None
			
	
	
		
	def StateGet(o):
		D = o.__dict__.copy()
		del D["Thread"]
		del D["Queue"]
		del D["Active"]
		del D["Parent"]
		return D

	def StateSet(o, D):
		for E, V in D.items(): setattr(o, E, V)

			
		
	def Start(o):
		pass

	# def Pulse(o):
	# 	pass

	def Free(o):
		pass


		
	_DirectAttributes = set(("Thread", "Queue", "Active", "Execute", "ExecuteWaitReturn"))	
	
	def __getattribute__(o, Name):
		# Say_("Get:", Name)
		A = object.__getattribute__(o, Name)
		if Name[0] == "_" or Name in Parallel._DirectAttributes or o.Thread is threading.currentThread():
			return A
		else:
			if hasattr(A, "__call__"):
				# Say_("Parallel Function Get:", Name)
				def F(*L, **D):
					if D.pop("WaitReturn", False):
						return o.ExecuteWaitReturn(A, *L, **D)
					else:
						o.Execute(A, *L, **D)
				F.Parallel = o
				return F
			else:
				# Say_("Parallel Get:", Name)
				return o.ExecuteWaitReturn(object.__getattribute__, o, Name)

	def __setattr__(o, Name, Value):
		# Say_("Set:", Name, Value)
		if Name[0] == "_" or Name in Parallel._DirectAttributes or o.Thread is threading.currentThread():
			object.__setattr__(o, Name, Value)
		else:
			# Say_("Parallel Set:", Name, Value)
			o.Execute(object.__setattr__, o, Name, Value)
				
				


# @Omnipresent
# def ParallelReceiver(Function):
	# return lambda *L, **D: L[0].Execute(Function, *L, **D)



@Omnipresent
def BaseReceiver(Function):
	return lambda *L, **D: Base.Execute(Function, *L, **D)



def Execute(*L, **D):
  try:
    if L[0].__class__ is str: exec(L[0], globals(), D)
    else: L[0](*L[1:], **D)
  except Exception as E: Say(E)




def Current():
	T = threading.currentThread()
	with ParallelsLock: P = Parallels[T]
	return P


class Base(Parallel):

	def __init__(o):
		o.Queue = queue.Queue()
		o.Active = o._Active = True
		o.Thread = threading.currentThread()
		Parallels[o.Thread] = o
		o.PulseRate = 60
		o.Pulses = []

		
	def Start(o, E = None):

		if E is None: pass
		elif isinstance(E, type): E()
		elif type(E) is types.FunctionType:
			class P(Parallel):
				def Start(o):
					E()
			P()
		else:
			raise Exception("Unable to start: " + str(E))
		
		while o.Active:
			
			o.Yield(1 / o.PulseRate)	
			
			for F in o.Pulses: F()
			
			with ParallelsLock: 
				if len(Parallels) == 1: break
			
			
	def End(o):
		if o._Active:
			o._Active = False
			
			# Say("E N D +++++++++++++++++++:")

			while True:
				
				with ParallelsLock: 
					if len(Parallels) == 1: break
					L = Parallels.copy().values()
				
				for P in L: P.End()
				
				o.Yield(.1)
			
			o.Active = False

			# import os
			# os._exit(1)		
		
		
Omnipresent.Base = Base = Base()



@Omnipresent
def ProgramStart(E):
	if E.__module__ == "__main__": 
		Base.Start(E)
	else: 
		return E