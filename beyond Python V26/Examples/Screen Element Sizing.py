import beyond.Reaper
import beyond.Screen


@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("Screen Element Sizing")
		e.Position(50, 50)

		e.Button("Add", "Default Size")

		e.Button("Add", "200 x 100 Size")
		e.Size(200, 100)

		e.Button("Add", "StretchWidth x 100 Size")
		e.Size(200, 100)
		e.StretchWidth()

		e.Button("Add", "200 x StretchHeight Size")
		e.Size(200, 100)
		e.StretchHeight()

		e.Text("TextEditor with Stretch() on both dimensions:")
		e.TextEditor("Editor")
		e.Size(600, 200)
		e.Stretch()

		with e.HorizontalRight():
			e.Text("Resize the Window to see Stretching >>")


	def Add(o):
		o.Editor.Insert("Add Text\n")