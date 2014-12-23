import beyond.Reaper
import beyond.Screen

@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("beyond Python")

		e.Text("Hello World!")
		e.Font("Helvetica 80 italic")
		e.Color("Purple")
		e.Padding(20)

		with e.HorizontalRight():
			e.Button("Again")


	def Again(o):
		Say("Hello Again")