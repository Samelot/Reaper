import beyond.Reaper
import beyond.Screen
import beyond.File


@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("Data Saving and Loading")

		with e.Horizontal():
			e.Text("Data Saving & Loading")
			e.Font("Helvetica 30")
			e.Color("Maroon")
			e.Padding(10, 5, 20, 20)


		with e.Horizontal():
			e.Padding(10)
			e.Size(600, 200)
			e.Stretch()

			with e.Vertical():
				e.Slider("Volume", 0.0, -60.0, 24.0)
				e.TextInput("Volume")
				e.Switch("Solo")
				e.Switch("Mute")

			e.Text("Name:")
			e.TextInput("Name")

			e.Text("   Comments:")
			e.TextEditor("Comments")
			e.Stretch()


		with e.HorizontalRight():
			e.Text("File:")
			e.TextInput("FilePath", (ProgramDirectory / "State").Path)
			e.Size(400, 24)
			e.Button("Save")
			e.Button("Load")


	def Save(o):
		o.StateSave(File(o.FilePath))

	def Load(o):
		Previous = o.FilePath
		o.StateLoad(File(o.FilePath))
		o.FilePath = Previous

	def Input(o, Name, Value):
		Say("Input:", Name, Value)

	def InputEnd(o):
		Say("Ending:")
		Base.End()