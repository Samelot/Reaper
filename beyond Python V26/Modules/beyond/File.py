import beyond.Class
import os, os.path, sys, imp


@Omnipresent
class File():

	def __init__(o, Path):
		o.Path = Path
	
	@Property
	def Path(o, p):
		if p.Get:
			p.Value = os.path.join(o.ParentPath, o.NameVersion + o.Extension)

		elif p.Set:

			o.ParentPath, N = os.path.split(p.Value)
			N, o.Extension = os.path.splitext(N)

			o.Version = 0
			i = N.rfind(" V")
			if i != -1:
				try:
					o.Version = int(N[i + 2:])
					N = N[0:i]
				except: pass
				
			o.Name = N
	

	@Property
	def NameVersion(o, p):
		p.Value = o.Name
		if o.Version > 0: p.Value += " V" + str(o.Version)
		
	@Property
	def Parent(o, p):
		p.Value = File(o.ParentPath)
		if p.Value.Name == "": p.Value = None

	def __truediv__(o, Name):
		return File(os.path.join(o.Path, Name))
	
	def __iter__(o):
		for N in os.listdir(o.Path):
			yield File(os.path.join(o.ParentPath, N))

	def __hash__(o):
		return o.Path.__hash__()

	def __eq__(o, o2):
		return o.Path == o2.Path

	def __str__(o):
		return '"' + o.Path + '"'


	@Property	
	def IsFile(o, p):
		p.Value = os.path.isfile(o.Path)
		
	@Property
	def IsDirectory(o, p):
		p.Value = os.path.isdir(o.Path)
		
	@Property
	def Binary(o, p):
		if p.Get:
			with open(o.Path, "rb") as F: p.Value = F.read()
		elif p.Set:
			with open(o.Path, "wb") as F: F.write(p.Value)
		
		
	def LastVersion(o):
		for F in o.Parent: 
			if F.Name == o.Name and F.Version > o.Version: o.Version = F.Version
	
	def NextVersion(o):
		o.LastVersion()
		o.Version += 1
	
	
	def ParentFind(o, Name):
		F = File(os.path.join(o.Path if o.IsDirectory else o.ParentPath, Name))
		# Say(F)
		if F.IsFile or F.IsDirectory: return F
		else:
			P = o.Parent
			if P is None: return None
			else: return P.ParentFind(Name)
					


	def Import(o):
		S = sys.dont_write_bytecode
		sys.dont_write_bytecode = True
		if o.ParentPath not in sys.path: sys.path.append(o.ParentPath)
		M = imp.load_source(o.Name, o.Path)
		sys.dont_write_bytecode = S
		return M

	def Execute(o):
		Source = o.Binary.decode("utf-8")
		C = compile(Source, o.Path, 'exec')
		if o.ParentPath not in sys.path: sys.path.append(o.ParentPath)
		G = sys._getframe(1).f_globals
		exec(C, G, G)


def _Import(o):
	File.__module__ = "beyond"
	beyond.File = File

Omnipresent.ProgramDirectory = File(sys.path[0])