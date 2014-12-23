import beyond.Reaper
import beyond.Reaper.Track
import beyond.Screen


@ProgramStart
class Main(Parallel):

  def Start(o):

    with Reaper as r:

      Project = r.ProjectSelected

      Project.UndoEvent("Modify Effect Envelopes Example")

      for Track in Project.TracksSelected:

        Say("Selected Track:", Track.Name)
        Say()

        Track.Receive()

        for Effect in Track.Effects:

          Say("Effect Name:", Effect.Name)
          Say("Plugin:", Effect.Plugin)
          Say()

          for E in Effect.Elements:
            if E.Name == ("PARMENV"):
            
              Say("Parameter Number:", E.PARMENV[0])
              Say("Armed:", E.ARM)
              Say("Lane Height:", E.LANEHEIGHT[0])
              Say("Visible:", E.VIS[0])
              Say("All Elements:", E)

              Say("Modifying Envelope Points (PT):")
              for e in E:
                if e.Name == "PT":

                  Say("Time:", e[0], "Value:", e[1])

                  e[0] += 1

              Say()

          Say()


        Track.Send()