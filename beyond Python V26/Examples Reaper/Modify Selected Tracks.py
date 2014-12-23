import beyond.Reaper
import beyond.Reaper.Track
import beyond.Screen


@ProgramStart
class Main(Parallel):

	def Start(o):

		with Reaper as r:

			Project = r.ProjectSelected

			Project.UndoEvent("Modify Selected Tracks Example")

			for T in Project.TracksSelected:

				Say("Selected Track:", T.Name)
				Say()

				T.Receive()

				Say("Pythonized Track Elements:", T.Elements)
				Say()

				T.Elements.VOLPAN[0] *= .9
				T.Elements.VOLPAN[1] += .1

				Say("Effects:")
				for E in T.Effects:
					Say(E.Name, "Active:", E.Active, "Online:", E.Online)
					E.Active = not E.Active

				T.Name +=	"!"

				T.Send()