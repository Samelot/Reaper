import beyond.Reaper
import beyond.Screen


@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("Layout Examples")

		with e.HorizontalCenter():
			e.Text("Layouts")
			e.Font("Helvetica 50 italic")
			e.Color("Dark Green")
			e.Padding(200, 20)

		with e.HorizontalCenter("HorizontalCenter with a Frame and Title"):
			e.SliderHorizontal("X", 0.0, -1.0, 1.0)
			e.TextInput("X")
			e.Button("Zero", "0")

		with e.Horizontal("Horizontal"):
			e.SliderHorizontal("X", 0.0, -1.0, 1.0)
			e.TextInput("X")
			e.Button("Zero", "0")

		with e.HorizontalRight("HorizontalRight"):
			e.SliderHorizontal("X", 0.0, -1.0, 1.0)
			e.TextInput("X")
			e.Button("Zero", "0")

		with e.Vertical("Vertical"):
			e.Slider("X", 0.0, -1.0, 1.0)
			e.TextInput("X")
			e.Button("Zero", "0")

		with e.HorizontalCenter():
			with e.Vertical("Vertical inside HorizontalCenter"):
				e.Slider("X", 0.0, -1.0, 1.0)
				e.TextInput("X")
				e.Button("Zero", "0")


	def Zero(o):
		o.X = 0