import beyond.Parallel
import	tkinter
from tkinter import ttk
import threading, io, pickle



@Omnipresent
class Screen(beyond.Statable):

	def __init__(o, Parent = None, Embed = False, **D):
		
		o.__dict__["Parent"] = Parent
		o.__dict__.update(D)
				
		o._Engine = e = tkEngine()
		e.Owner = o
		e.Embed = Embed
		e.Settings = {}
		e.Children = {}
		e.PropertySetters = {}
		e.PropertySetters["Visible"] = o._SetVisible
		if "Visible" not in o.__dict__: o.__dict__["Visible"] = True
		e.Title("beyond Screen")
		
		if Parent is None or not Embed:
			e.Parallel = beyond.Parallel.Parallel(Stay = True)
			e.Parallel.Thread.name = o.__class__.__name__
			e.Parallel.Execute(e.Construct)
		else:
			e.Parallel = Parent._Engine.Parallel


	def _SetVisible(o, Visible):
		if Visible: o._Engine.Show()
		else: o._Engine.Hide()






	def Wait(o, Duration):
		o._Engine.Parallel.Yield(Duration)



	def __getattribute__(o, Name):
		# Say_("Get:", Name)
		A = object.__getattribute__(o, Name)
		if Name[0] == "_": return A

		e = Screen.__getattribute__(o, "_Engine")
		if e.AllowDirectAccess():
			return A
		else:
			P = e.Parallel
			if hasattr(A, "__call__"):
				# Say_("Parallel Function Get:", Name)
				def F(*L, **D):
					if D.pop("WaitReturn", False):
						return P.ExecuteWaitReturn(A, *L, **D)
					else:
						P.Execute(A, *L, **D)
				F.Parallel = P
				return F
			else:
				# Say_("Parallel Get:", Name)
				return P.ExecuteWaitReturn(object.__getattribute__, o, Name)


	def __setattr__(o, Name, Value):
		# Say_("Set:", Name, Value)
		if Name[0] == "_":
			object.__setattr__(o, Name, Value)
		else:
			e = o._Engine
			if e.AllowDirectAccess():
				o._Parallel_Set(Name, Value)
			else:
				# Say("Parallel Set:", Name, Value)
				e.Parallel.Execute(o._Parallel_Set, Name, Value)

	def _Parallel_Set(o, Name, Value):
		P = o._Engine.PropertySetters.get(Name, None)
		if P is not None:
			OldValue = object.__getattribute__(o, Name)
			if Value != OldValue: P(Value)
		object.__setattr__(o, Name, Value)




	def StateGet(o):
		D = o.__dict__.copy()
		del D["_Engine"]
		del D["Parent"]
		return D

	def StateSet(o, D):
		for E, V in D.items(): setattr(o, E, V)		
		
		
		
		
	def	Setup(o, e):
		e.Text("beyond Screen!")	
		
	def Input(o, Name, Value):
		# Say(Name, Value)
		pass

	def InputEnd(o):
		Base.End()	
		
	def Free(o):
		# Say("Free Screen:", o)
		for S in o._Engine.Children.values(): S.Free()










class tkEngine():

	def __init__(o):
		o.tkVariables = {}
		o.BaseDirectAccess = False

	def AllowDirectAccess(o):
		T = threading.currentThread()
		return T == o.Parallel.Thread or (o.BaseDirectAccess and T is Base.Thread)

	def Construct(o):
		Base.ExecuteWaitReturn(o._Base_Construct)

	def _Base_Construct(o):

		if not hasattr(Base, "Tk"):
			Base.Tk = tkinter.Tk()
			Base.Tk.withdraw()
			Base.Pulses.append(lambda: Base.Tk.update())

		o.tkToplevel = o.tkWidget = tkinter.Toplevel(Base.Tk)
		o.tkWidget.protocol("WM_DELETE_WINDOW", lambda: o.Owner.InputEnd())

		o.ContainerStack = []
		with o._Container(o):
			o.BaseDirectAccess = True
			o.Owner.Setup(o)
			if not o.Owner.Visible: o.tkToplevel.withdraw()
			o.BaseDirectAccess = False

		o.tkToplevel.title(o.TitleText)

		# o.tkToplevel.update()
		# Say(o.tkToplevel.geometry())

		o.Parallel.Free = o.Free

	def Show(o):
		if not o.Embed:
			Base.Execute(o.tkToplevel.deiconify)


	def Hide(o):
		if not o.Embed:
			Base.Execute(o.tkToplevel.withdraw)


	def Free(o):
		# Say_("Free Engine:", o.Owner)
		o.Owner.Free()
		Base.Execute(o.tkToplevel.destroy)
		o.tkToplevel = None



	def Screen(o, Name, ScreenClass = None):

		if ScreenClass is None:
			ScreenClass = Name
			Name = ScreenClass.__name__

		o._ScreenPending()
		if Name in o.Owner.__dict__:
			S = o.Owner.__dict__[Name]
		else:
			S = ScreenClass(o.Owner, Embed = True)
			o.Children[Name] = S
		o.Container.ScreenPending = S
		o.Property(Name, S)
		o.tkWidget = o.tkWidgetFrame = F = ttk.Frame(o.Container.tkWidget)
		F.columnconfigure(0, weight = 1)
		F.rowconfigure(0, weight = 1)
		o.LastLayout = o.Container.Layout
		o.LastLayout(o)
		return S

	def _ScreenPending(o):
		S = o.Container.ScreenPending
		if S is not None:
			o.Container.ScreenPending = None
			with o._Container(o):
				e = S._Engine
				e.ContainerStack = o.ContainerStack
				e.Container = o.Container
				e.tkWidgetFrame = o.tkWidgetFrame
				e.LastLayout = o.LastLayout
				e.BaseDirectAccess = True
				S.Setup(e)
				e.BaseDirectAccess = False


	def Tabs(o, *ScreenClasses, Padding = 4):
		o._ScreenPending()
		N = o.tkAdd(ttk.Notebook)
		for C in ScreenClasses:
			S = o.Screen(C)
			o._ScreenPending()
			o.Padding(Padding)
			N.add(o.tkWidgetFrame, text = S._Engine.TitleText)
		o.tkWidget = o.tkWidgetFrame = N
		o.Padding(2)


	def Title(o, Text):
		o.TitleText = Text


	def Position(o, X, Y):
		if not o.Embed and o.tkWidget is o.tkToplevel:
			o.tkToplevel.geometry("+" + str(X) + "+" + str(Y))



	class _Container:
		
		def __init__(o, e):
			o.e = e
			o.tkWidget = e.tkWidget
			o.Layout = tkEngine.tkLayoutVertical
			o.ScreenPending = None
			e.ContainerStack.append(o)
			e.Container = o
		
		def __enter__(o):
			pass
				
		def __exit__(o, ExceptionType, Exception, Traceback):
			e = o.e
			e._ScreenPending()
			del e.ContainerStack[-1]
			e.Container = e.ContainerStack[-1] if len(e.ContainerStack) > 0 else None

		
	
	def Vertical(o, Text = None):
		if Text is None: o.tkAddFramed(ttk.Frame)
		else: o.tkAddFramed(ttk.Labelframe, text = Text)
		return o._Container(o)
	
	def Horizontal(o, Text = None):
		C = o.Vertical(Text)
		o.tkWidgetFrame.pack(anchor = "nw")
		o.Container.Layout = tkEngine.tkLayoutHorizontal
		return C
	
	def HorizontalRight(o, Text = None):
		C = o.Vertical(Text)
		o.tkWidgetFrame.pack(anchor = "ne")
		o.Container.Layout = tkEngine.tkLayoutHorizontal
		return C
	
	def HorizontalCenter(o, Text = None):
		C = o.Vertical(Text)
		o.tkWidgetFrame.pack(anchor = "n")
		o.Container.Layout = tkEngine.tkLayoutHorizontal
		return C

	
	def tkLayoutVertical(o):
		o.tkWidgetFrame.pack(anchor = "nw")

	def tkLayoutHorizontal(o):
		o.tkWidgetFrame.pack(side = "left", anchor = "nw")

		
		

	def tkAdd(o, tkWidgetClass, **D):
		o._ScreenPending()
		o.tkWidget = o.tkWidgetFrame = tkWidgetClass(o.Container.tkWidget, **D)
		o.LastLayout = o.Container.Layout
		o.LastLayout(o)
		return o.tkWidget

	def tkAddFramed(o, tkWidgetClass, **D):
		o._ScreenPending()
		o.tkWidgetFrame = F = ttk.Frame(o.Container.tkWidget)
		o.tkWidget = tkWidgetClass(F, **D)
		o.tkWidget.pack(fill = "both", expand = True)
		o.LastLayout = o.Container.Layout
		o.LastLayout(o)
		return o.tkWidget

	def tkSet(o, **D):
		o.tkWidget.config(**D)



	def Button(o, Property, Text = None):
		if Text is None: Text = Property
		o.tkAddFramed(ttk.Button, text = Text)
		try:
			F = o.Owner.__class__.__dict__[Property]
			o.tkWidget["command"] = lambda: o.Parallel.Execute(F, o.Owner)
		except:
			Say("Button Function not defined:", Property)

	def Text(o, Property, Value = None):
		if Value is None: Property, Value = None, Property
		if Property is None:
			o.tkAddFramed(ttk.Label, text = str(Value))
		else:
			o.tkAddFramed(ttk.Label)
			o.Property(Property, Value, "textvariable")

	def TextInput(o, Property, Value = ""):
		o.tkAddFramed(ttk.Entry)
		o.Property(Property, Value, "textvariable")

	def Switch(o, Property, State = False, Text = None):
		if Text is None: Text = Property
		o.tkAddFramed(ttk.Checkbutton, text = Text)
		o.Property(Property, State)

	def Slider(o, Property, Value = 0, From = 0, To = 1):
		o.tkAddFramed(ttk.Scale, from_ = To, to = From, orient = "vertical")
		o.Property(Property, Value)

	def SliderHorizontal(o, Property, Value = 0, From = 0, To = 1):
		o.tkAddFramed(ttk.Scale, from_ = From, to = To)
		o.Property(Property, Value)


	def Property(o, Name, Default = "", tkSetting = "variable"):

		if Name in o.Owner.__dict__:
			Value = o.Owner.__dict__[Name]
		else:
			Value = Default
			o.Owner.__dict__[Name] = Value

		if o.Container.ScreenPending is None:

			if Name in o.tkVariables:
				V = o.tkVariables[Name]
			else:
				T = Value.__class__
				if T is str: V = tkinter.StringVar()
				elif T is float: V = tkinter.DoubleVar()
				elif T is int: V = tkinter.IntVar()
				elif T is bool: V = tkinter.BooleanVar()
				V.Name = Name
				V.set(Value)
				V.Supress = 0
				V.trace("w", lambda *L: o._Base_VariableGet(V))
				o.tkVariables[Name] = V
				o.PropertySetters[Name] = lambda Value: Base.Execute(tkEngine._Base_VaribleSet, V, Value)

			o.tkWidget[tkSetting] = V

		else:
			o.Set(Property = Name)

	def _Base_VariableGet(o, V):
		if V.Supress > 0:
			V.Supress -= 1
		else:
			try:
				o.Parallel.Execute(o._Parallel_VariableTrace, V.Name, V.get())
			except:
				pass

	def _Parallel_VariableTrace(o, Name, Value):
		OldValue = o.Owner.__dict__[Name]
		# Say("Variable:", Name, Value, OldValue)
		if Value != OldValue:
			o.Owner.__dict__[Name] = Value
			o.Owner.Input(Name, Value)

	def _Base_VaribleSet(V, Value):
		V.Supress += 1
		V.set(Value)



	def Size(o, Width, Height):
		o.tkWidgetFrame.pack_propagate(False)
		o.tkWidgetFrame.config(width = Width, height = Height)

	def Stretch(o):
		o.tkWidgetFrame.pack(fill = "both", expand = True)

	def StretchWidth(o):
		o.tkWidgetFrame.pack(fill = "x", expand = o.LastLayout is tkEngine.tkLayoutHorizontal)

	def StretchHeight(o):
		o.tkWidgetFrame.pack(fill = "y", expand = o.LastLayout is tkEngine.tkLayoutVertical)

	def Padding(o, *L):
		o.tkWidgetFrame.config(padding = L)


	def Color(o, Foreground, **D):
		o.tkSet(foreground = Foreground)

	def Font(o, Font):
		if o.Container.ScreenPending is None:
			o.tkSet(font = Font)
		else:
			o.Set(Font = Font)

	def Set(o, **D):
		if o.Container.ScreenPending is not None:
			o.Container.ScreenPending._Engine.Settings.update(D)





	def TextEditor(o, Name):
		return o.Screen(Name, TextEditor)






class ScrollableWidget:

	def __init__(o, e, WidgetClass, Frame = None):

		if Frame is not None:
			Frame.grid_propagate(False)
			Frame.columnconfigure(0, weight = 1)
			Frame.rowconfigure(0, weight = 1)

		o.Widget = e.tkAdd(WidgetClass)
		o.Widget.grid(column = 0, row = 0, sticky = "nwse")
		o.Widget["xscrollcommand"] = o.Update
		o.Widget["yscrollcommand"] = o.Update

		o.ScrollX = e.tkAdd(ttk.Scrollbar, orient = "horizontal")
		o.ScrollX.grid(column = 0, row = 1, sticky = "nwse")
		o.ScrollX["command"] = o.Widget.xview

		o.ScrollY = e.tkAdd(ttk.Scrollbar)
		o.ScrollY.grid(column = 1, row = 0, rowspan = 2, sticky = "nwse")
		o.ScrollY["command"] = o.Widget.yview


		e.tkWidget = o.Widget

		o.ScrollXVisible = True
		o.ScrollYVisible = True
		o.SupressUpdate = 0


	def Update(o, *L):

		# Say_("=====================================:")

		if o.SupressUpdate > 0:
			o.SupressUpdate -= 1
			# Say_("Supress:", o.SupressUpdate)
		else:

			o.X = o.Widget.xview()
			o.Y = o.Widget.yview()

			# Say_("X:", o.X)
			# Say_("Y:", o.Y)

			o.ScrollX.set(*o.X)
			o.ScrollY.set(*o.Y)

			if o.X[0] <= 0.0 and o.X[1] >= 1.0:
				if o.ScrollXVisible:
					# Say_("HIDE:", o.ScrollXVisible)
					o.ScrollX.grid_remove()
					o.ScrollXVisible = False

					Old = o.X
					o.SupressUpdate = 2
					o.Widget.master.update_idletasks()
					o.X = o.Widget.xview()
					# Say_("X 2:", o.X)

					if not (o.X[0] <= 0.0 and o.X[1] >= 1.0):
						# Say_("RESTORE:", Old)
						# o.ScrollX.set(*Old)
						o.ScrollX.set(0.0, 1.0)
						o.ScrollX.grid()
						o.ScrollXVisible = True
						o.SupressUpdate = 2

			elif not o.ScrollXVisible:
				# Say_("SHOW:", o.ScrollXVisible)
				o.ScrollX.grid()
				o.ScrollXVisible = True



			if o.Y[0] <= 0.0 and o.Y[1] >= 1.0:
				if o.ScrollYVisible:
					o.ScrollY.grid_remove()
					o.ScrollYVisible = False

					o.SupressUpdate += 2
					o.Widget.master.update_idletasks()
					o.Y = o.Widget.yview()

					if not (o.Y[0] <= 0.0 and o.Y[1] >= 1.0):
						o.ScrollY.set(0.0, 1.0)
						o.ScrollY.grid()
						o.ScrollYVisible = True
						o.SupressUpdate += 2

			elif not o.ScrollYVisible:
				o.ScrollY.grid()
				o.ScrollYVisible = True




class TextEditor(Screen):

	def Setup(o, e):

		# Say(e.Settings)

		ScrollableWidget(e, tkinter.Text, e.tkWidgetFrame)
		e.tkSet(wrap = "none", font = e.Settings.pop("Font", "Times 10"))

		C = e.Settings.pop("ColorBack", None)
		if C is not None: e.tkSet(background = C)

		C = e.Settings.pop("ColorFront", None)
		if C is not None: e.tkSet(foreground = C)


		if "Text" in o.__dict__: o.Insert(o.Text)
		e.tkText = e.tkWidget



	def Test(o):
		# o.Text += "1234"
		Say(o)
		Say(o.__dict__)
		Say(o._Engine)


	def Insert(o, Text, Position = "end"):
		Base.Execute(o._Engine.tkText.insert, Position, str(Text))

	def Show(o, Position = "end"):
		Base.Execute(o._Engine.tkText.see, Position)

	def GetText(o, Start = "1.0", End = "end - 1c"):
		return Base.ExecuteWaitReturn(o._Engine.tkText.get, Start, End)


	def __setattr__(o, Name, Value):
		# Say_("Set:", Name, Value)
		if Name == "Text" and "tkText" in o._Engine.__dict__:
			Base.Execute('T.delete("1.0", "end")\nT.insert("1.0", Text)', T = o._Engine.tkText, Text = str(Value))
		else:
			o.__dict__[Name] = Value
			# object.__setattr__(o, Name, Value)

	def __getattribute__(o, Name):
		# Say_("Get:", Name)
		if Name == "Text" and "tkText" in o._Engine.__dict__:
			return o.GetText()
		else:
			return object.__getattribute__(o, Name)



	def Free(o):
		o.__dict__["Text"] = o.GetText()
		del o._Engine.tkText
		# Say("Free Editor:", o, o.Text)


	def StateGet(o):
		return {"Text": o.GetText()}

		


class SayScreen(Screen):

	def Setup(o, e):
		e.Title("Messages:")
		e.Position(1300, 0)
		e.TextEditor("Editor")
		e.Size(600, 1000)
		e.Stretch()
		e.Font("Courier 9")
		e.Set(ColorBack = "#1C0500", ColorFront = "#FB0")
		# e.Set(ColorBack = "#106", ColorFront = "#A8F")
		o.Ready = True

	def Add(o, Text):
		if o.Ready:
			o.Visible = True
			o.Editor.Insert(Text)
			o.Editor.Show()

	def InputEnd(o):
		with beyond.Parallel.ParallelsLock: C = len(beyond.Parallel.Parallels)
		if C == 2: Base.End()
		else: o.Visible = False

	def Free(o):
		o.Ready = False
		Screen.Free(o)


SayScreenActive = None

def SayOutput(Text):

	global SayScreenActive
	if SayScreenActive is None: SayScreenActive = SayScreen(Ready = False)

	SayScreenActive.Add(Text)
	# SayScreenActive._Engine.Parallel.Execute(SayScreenActive.Add, Text)
	# SayScreenActive._Engine.Parallel.Execute("o.Add(Text)", o = SayScreenActive, Text = Text)


beyond.Text.SayOutputs.append(SayOutput)

