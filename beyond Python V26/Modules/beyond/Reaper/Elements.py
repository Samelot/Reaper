import beyond.Elements
import base64, io



class Element(beyond.Elements.Element):
	
	__PropertiesNative__ = "Name", "_ValuesSerialized", "_Serialize", "_Deserialize", "_List"

	def __Object__(c, Name, ValuesSerial):
		o = c.Base()
		o.Name = Name
		o.ValuesSerial = ValuesSerial

		
	def _Serialize(o, s, Full = True):

		Previous = False

		if Full and o.Name != "":
			s += o.Name
			Previous = True
							
		if o._ValuesSerialized:
			if Previous: s += " "
			s += o.ValuesSerial

		else:

			ValuesStart = s.tell() + (1 if Previous else 0)

			for E in o._List:

				if Previous: s += " "
				
				C = type(E)
				
				if C is int:
					s += str(E)
				
				elif C is float:
					s += str(E)
				
				elif C is ID:
					s += "{"
					s += str(E)
					s += "}"

				elif C is str:
					
					Q = 0
					
					for C in E:
						if C == '"': Q |= 1
						elif C == "'" : Q |= 2
						elif C == "`" : Q |= 4
						if Q == 7: break
							
					if Q & 1 == 0: Q = '"'
					elif Q & 2 == 0: Q = "'"
					elif Q & 4 == 0: Q = "`"
					else:
						Q = "`"
						E = E.replace(Q, "'")
						
					s += Q
					s += E
					s += Q
				
				elif C is bool:
					s += str(int(E))

				elif C is Word:
					s += str(E)

				else:
					s += "-"

				Previous = True

			End = s.tell()
			s.seek(ValuesStart)
			o.ValuesSerial = s.read()
			s.seek(End)

		if Full:
			s += "\n"


	def _Deserialize(o):

		o._List = []

		ValuesSerial = o.ValuesSerial
		Start = i = 0
		EndQuote = ""
		
		def Add():
			E = ValuesSerial[Start:i]
			if EndQuote == "}": o._List.append(ID(E))
			elif EndQuote != "": o._List.append(E)
			elif Start < i:
				E = beyond.Text.ToNumber(E)
				if type(E) is str: o._List.append(Word(E))
				else: o._List.append(E)
			return i + 1
				
		for C in ValuesSerial:
			if EndQuote == "":
				if C in "\"'`":
					EndQuote = C
					Start = i + 1
				elif C == "{":
					EndQuote = "}"
					Start = i + 1					
				elif C in " \r\t":
					if Start < i: Start = Add()
					else: Start = i + 1	
			elif C == EndQuote:
				Start = Add()
				EndQuote = ""
			i += 1
		Add()

		o._ValuesSerialized = False

	
	@Property
	def ValuesSerial(o, p):
		if p.Get:
			if o._ValuesSerialized:
				p.Base()
			else:
				s = beyond.Text.Stream()
				o._Serialize(s, False)
				p.Value = s.Complete()
		elif p.Set:
			o._ValuesSerialized = True
			p.Base()


	def __getitem__(o, Index):
		if o._ValuesSerialized: o._Deserialize()
		return o._List.__getitem__(Index)

	def __setitem__(o, Index, Value):
		if o._ValuesSerialized: o._Deserialize()
		if Index >= len(o):
			for i in range(Index - len(o) + 1): o._List.append(None)
		o._List.__setitem__(Index, Value)

	def __delitem__(o, Index):
		if o._ValuesSerialized: o._Deserialize()
		o._List.__delitem__(Index)

	def __len__(o):
		if o._ValuesSerialized: o._Deserialize()
		return o._List.__len__()

	def __iter__(o):
		if o._ValuesSerialized: o._Deserialize()
		return o._List.__iter__()

	def __reversed__(o):
		if o._ValuesSerialized: o._Deserialize()
		return o._List.__reversed__()



class ID(str):
	pass

class Word(str):
	pass	

WordBlank = Word()




class Elements(beyond.Elements.Elements):
	
	__PropertiesNative__ = "Binary", "_Serialize", "_Deserialize"
	
	def __Object__(c, Serial = None):
		o = c.Base()
		if Serial is None: o.Binary = None	
		else: o.Serial = Serial

		
	def _Serialize(o, s):
		s += "<"
		for E in o: E._Serialize(s)
		if o.Binary is not None: s += base64.encodebytes(o.Binary).decode("utf-8")
		s += ">\n"
	
	
	def _Deserialize(o, Text, Start = 0):
		
		o.Clear()
		o.Binary = None
		
		i = SpaceStart = DataStart = Start

		List, Name, Data, Binary = range(4)
		State = List
		EndQuote = ""
	
		def Add():
			if State == Name or State == Data:

				if Start < SpaceStart:
					N = Text[Start:SpaceStart]
					D = Text[SpaceStart + 1:i].rstrip()
				else:
					N = Text[Start:i]
					D = ""

				if D == "" and len(o) == 1 and (N[-1] == "=" or not N.isupper()):
					return Binary
				elif N[0] in "0123456789.-":
					o.Add(Element("", Text[Start:i]))
					return List
				else:
					o.Add(Element(N, D))
					return List

			else: return State


		while i < len(Text):
		
			C = Text[i]
			
			if State == Binary:
				i = Text.find(">", i)
				D = Text[Start:i]
				D = D.encode("utf-8")
				D = D.rstrip()
				l = len(D)
				f = D.rfind(b"==", 0, l - 1 if D.endswith(b"==") else l + 1)
				if f != -1 and l - f > 2:
					B = io.BytesIO() 
					for L in D.split(b"\n"):
						B.write(base64.decodebytes(L))
					o.Binary = B.getvalue()
					B.close()
				else:
					o.Binary = base64.decodebytes(D)
				break

			elif C in " \r\t\n\"'`<>":

				if C in "\"'`":
					if EndQuote == "":
						EndQuote = C
					elif C == EndQuote:
						EndQuote = ""

				elif EndQuote != "":
					pass
			
				elif C in " \r\t":
					if State == Name:
						SpaceStart = i
						State = Data

				elif C in "\n":
					State = Add()
					
				elif C in "<":
					State = Add()
					E = Elements()
					i = E._Deserialize(Text, i + 1)
					o.Add(E)
						
				elif C in ">":
					Add()
					break

			elif State == Name or EndQuote != "":
				pass
			elif State == List:
				State = Name
				Start = i
					
			i += 1
		
		return i


	@Property
	def Serial(o, p):
		if p.Get:
			s = beyond.Text.Stream()
			o._Serialize(s)
			p.Value = s.Complete()
		elif p.Set:
			o._Deserialize(p.Value)


	def __PropertiesDynamic__(o, p):
		Old = p.BaseGet()
		E = Old.Value if isinstance(Old.Value, beyond.Elements.Element) else None
		if Old.Exists and E is None:
			if p.Get: p.Value = Old.Value
			else: p.Base()
		else:
			if p.Get:
				if E is None: p.Exists = False
				elif isinstance(E, Elements): p.Value = E
				elif len(E) == 1: p.Value = E[0]
				elif len(E) == 0: p.Value = WordBlank
				else: p.Value = E
			elif p.Set:
				if isinstance(p.Value, beyond.Elements.Element): 
					if E is None:
						p.Value.Name = p.Name
						o.Add(p.Value)
					else:
						p.Base()
				else:
					if E is None: E = o.Add(Element(p.Name, ""))
					E[0] = p.Value
			elif p.Delete:
				p.Base()



	def Set(o, Name, Value, Index = 0):
		if isinstance(Value, beyond.Elements.Element): 
			super().Set(Name, Value)
		else:
			E = super().Get(Name)
			if E is None: E = o.Add(Element(Name, ""))
			E[Index] = Value




	@Property
	def Name(o, p):
		p.Base()
		if len(o) == 0:
			if p.Get: p.Value = ""
			elif p.Set: o.Add(Element(p.Value, ""))
		else:
			if p.Get: p.Value = o[0].Name
			elif p.Set: o[0].Name = p.Value
			
	
	
	def ReceiveFile(o, File):
		# TimerStart("ReceiveFile")
		o.Serial = File.Binary.decode("utf-8")
		# TimerEnd()
		return o


	def SendFile(o, File):
		File.Binary = o.Serial.encode("utf-8")
		return o



	def Say(o, s):
			
		s += "(Elements)"

		Seperator = "\n  "

		for E in o:
			if type(E) is Element:
				s += Seperator
				s += E.Name
				s += ": "
				s += E.ValuesSerial
			elif type(E) is Elements:
				s += Seperator
				s += "<"
				s += E.Name
				s += ">..."
				s += str(len(E))
		
		if o.Binary is not None:
			s += Seperator
			s += "+ Binary: "
			s += str(len(o.Binary))
	
		return "\n"

		


class Proxy(beyond.Reaper.Proxy):

	__PropertiesNative__ = "_InfoGet", "_InfoSet", "_InfoGetSetString", "_GetSet"

	def __Object__(c):
		o = c.Base()
		if c.New:
			o.Elements = beyond.Reaper.Elements.Elements()
			o.Connected = True
			o._ReceiveCapacity = 10 * 1024 ** 2

	@Property
	def Connected(o, p):
		p.Base()
		if p.Get: p.Value = p.Value and o.Address is not None

	def _GetSet(o, ElementName, ElementIndex, InfoName, DefaultValue, Set, SetValue):
		if Set:
			if ElementName is not None: o.Elements.Set(ElementName, SetValue, ElementIndex)
			if InfoName is not None and o.Connected:
				if InfoName[0] == "P": type(o)._InfoGetSetString(o.Address, InfoName, str(SetValue), True)
				else: type(o)._InfoSet(o.Address, InfoName, SetValue)
		else:
			if InfoName is not None and o.Connected:
				if InfoName[0] == "P": Value = type(o)._InfoGetSetString(o.Address, InfoName, "", False)[3]
				else: Value = type(o)._InfoGet(o.Address, InfoName)
				Value = type(DefaultValue)(Value)
				if ElementName is not None: o.Elements.Set(ElementName, Value, ElementIndex)
				return Value
			elif ElementName is not None and o.Elements.Has(ElementName):
				return type(DefaultValue)(o.Elements.Get(ElementName)[ElementIndex])
			else:
				return DefaultValue

