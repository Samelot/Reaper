import beyond.Reaper
import beyond.Screen


@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("Reaper Transport Example")

		with e.Horizontal():
			e.Stretch()
			
			e.Button("Play")
			e.Size(200, 200)
			e.Stretch()

			e.Button("Stop")
			e.Size(200, 200)
			e.Stretch()


	def Play(o):
		with Reaper as r: r.OnPlayButton()

	def Stop(o):
		with Reaper as r: r.OnStopButton()