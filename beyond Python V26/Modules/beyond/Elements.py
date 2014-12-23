import beyond.Class
import weakref



class Element(Class):
	
	__PropertiesNative__ = "Containers", "_Include", "_Exclude", "Copy"

	def __Object__(c):
		o = c.Base()
		o.Containers = weakref.WeakKeyDictionary()
		
	def __hash__(o):
		return id(o)

	def _Include(o, E):
		# Say("Include:", id(E))
		o.Containers.setdefault(E, 0)
		o.Containers[E] += 1

	def _Exclude(o, E):
		# Say("Exclude:", id(E))
		o.Containers[E] -= 1
		if o.Containers[E] <= 0: del o.Containers[E]

	@Property
	def Container(o, p):
		if len(o.Containers) == 1:
			for E in o.Containers: p.Value = E
		elif len(o.Containers) == 0:
			raise Exception("No Containers")
		else:
			raise Exception("Multipe Containers")

	def Copy(o, Copies = {}):
		# Say("Copy:", o)
		Copy = o.__class__.__new__(o.__class__)
		Copies[o] = Copy
		Copy.Containers = weakref.WeakKeyDictionary()
		for Name, Value in o.__dict__.items():
			if isinstance(Value, Element):
				if Value in Copies: E = Copies[Value]
				else: E = Value.Copy(Copies)
				Copy.__dict__[Name] = E
				E._Include(Copy)
			elif Name != "Containers":
				Copy.__dict__[Name] = Value
		return Copy


	@Property
	def Name(o, p):
		p.Base()
		if p.Set:
			for E in o.Containers: E._ElementRenamed(o)
		elif not p.Exists:
			p.Value = ""
			p.Exists = True
	
	@Property
	def Index(o, p):
		p.Value = o.Container._List.index(o)		


	def __PropertiesDynamic__(o, p):
		Old = p.BaseGet()
		if p.Get:
			p.Exists = Old.Exists
			p.Value = Old.Value
		else:
			if isinstance(Old.Value, Element): Old.Value._Exclude(o)
			if p.Set and isinstance(p.Value, Element): p.Value._Include(o)
			p.Base()



	
class Elements(Element):
	
	__PropertiesNative__ = "_List", "_Dictionary", "_DictionaryReady", "Get", "Set", "Add", "Remove", "Clear", "Has", "_ElementRenamed"
	
	def __Object__(c):
		o = c.Base()
		o._List = []
		o._Dictionary = {}
		o._DictionaryReady = True


	def Copy(o, Copies = {}):
		# Say("C:", o)
		Copy = super().Copy(Copies)
		Copy._List = []
		for E in o._List:
			if E in Copies: E = Copies[E]
			else: E = E.Copy(Copies)
			Copy._List.append(E)
			E._Include(Copy)
		Copy._Dictionary = {}
		Copy._DictionaryReady = False
		return Copy


	def Get(o, Name):
		D = o._Dictionary
		if not o._DictionaryReady:
			D.clear()
			for E in o._List: D.setdefault(E.Name, E)
			o._DictionaryReady = True
		return D.get(Name, None)

	def Set(o, Name, E):
		E.Name = Name
		Old = o.Get(Name)
		if Old is None: o.Add(E)
		else:
			Old._Exclude(o)
			o._List[o._List.index(Old)] = E
			o._Dictionary[Name] = E
			E._Include(o)

	def Add(o, E, Index = None):
		if Index is None: o._List.append(E)
		else: o._List.insert(Index, E)
		o._DictionaryReady = False
		E._Include(o)
		return E

	def Remove(o, E):
		E._Exclude(o)
		o._List.__delitem__(o._List.index(E))
		o._DictionaryReady = False
		return E

	def Clear(o):
		for E in o._List: E._Exclude(o)
		del o._List[:]
		o._Dictionary.clear()
		o._DictionaryReady = True

	def Has(o, Name):
		return o.Get(Name) is not None

	def _ElementRenamed(o, E):
		o._DictionaryReady = False


	
	def __PropertiesDynamic__(o, p):
		Old = p.BaseGet()
		if Old.Exists:
			if p.Get: p.Value = Old.Value
			else: p.Base()
		else:
			E = Elements.Get(o, p.Name)
			if E is None:
				if p.Get: p.Exists = False
				else: p.Base()
			else:
				if p.Get:
					p.Value = E
				elif p.Set:
					E._Exclude(o)
					p.Value.Name = p.Name
					o._List[o._List.index(E)] = p.Value
					o._Dictionary[p.Name] = p.Value
					p.Value._Include(o)
				elif p.Delete:
					o.Remove(E)


	def __getitem__(o, Index):
		return o._List.__getitem__(Index)

	def __setitem__(o, Index, E):
		o._List[Index]._Exclude(o)
		o._List.__setitem__(Index, E)
		o._DictionaryReady = False
		E._Include(o)

	def __delitem__(o, Index):
		o._List[Index]._Exclude(o)
		o._List.__delitem__(Index)
		o._DictionaryReady = False

	def __len__(o):
		return o._List.__len__()

	def __iter__(o):
		return o._List.__iter__()

	def __reversed__(o):
		return o._List.__reversed__()


