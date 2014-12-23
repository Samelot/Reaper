import beyond.Reaper
import beyond.Screen


@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("Screen Tabs")

		with e.Horizontal():
			e.Text("Tabs")
			e.Font("Helvetica 40 italic")
			e.Color("Dark Green")

		e.Tabs(o.Tab1, o.Tab2)
		e.Size(600, 400)
		e.Stretch()

		e.SliderHorizontal("X", 0, 0, 100)
		e.StretchWidth()


	class Tab1(Screen):

		def Setup(o, e):
			e.Title("Tab 1")
			e.Text("Hello...")
			e.Font("Helvetica 20")

			e.Text("Y", 0)
			

	class Tab2(Screen):

		def Setup(o, e):
			e.Title("Tab 2")
			e.Text("World!")
			e.Font("Helvetica 20")

			e.Button("AccessParent", "+")

		def AccessParent(o):
			o.Parent.X += 1
			o.Parent.Tab1.Y += 1