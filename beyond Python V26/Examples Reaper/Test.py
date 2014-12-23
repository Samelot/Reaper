import beyond.Reaper
import beyond.Screen


@ProgramStart
class Main(Parallel):

	def Start(o):

		Say("Connecting to Reaper:")

		with Reaper as r:

			Say("Connected:")
			Say()
			Say("Project Media Path:", r.GetProjectPath("", 512)[0])
			Say("Number of Tracks:", r.CountTracks(0))

			r.ShowConsoleMsg("Hello Reaper!\n")