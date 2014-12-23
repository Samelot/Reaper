import beyond.Reaper
import beyond.Reaper.Track
import beyond.Screen


@ProgramStart
class Main(Parallel):

  def Start(o):

    with Reaper as r:

      Project = r.ProjectSelected

      Project.UndoEvent("Track Reference Example")

      Project.Receive() # Quickly Receive the Track Hierarchy

      for T in Project:
        Say(":", T.Name)
        for t in T:
          Say("  :", t.Name, t.Index)

      # Say("Track by Name Path:", Project.Drums.Overhead.Selected) # Put in the Names from your Project
      # Say("by Any Name Path:", Project.Drums.Get("Overhead Left").Selected)

      Say()
      Say("Master Track Selected?:", Project.TrackMaster.Selected)

      Say()
      Say("Flip the Selection of all Tracks:")
      for T in Project.TracksAll:
        Say(T.Name, T.Address)
        T.Selected = not T.Selected

      # Project.TracksAll is a Fast Generator, great for breakable iterations, searches, etc..
      # Here is how to convert it into a regular list
      L = list(Project.TracksAll)
      Say("Track Count:", len(L))

      Say()
      if len(Project) >= 1:

        T = Project[0]
        Say("First Track in Hierarchy:", T.Name)
        if len(T) >= 2: Say("Second Child:", T[1].Name)
        
        Say()
        A = r.GetTrack(Project.Address, 0) # Directly From Reaper API
        T = r.Track(A) # Make it into a beyond.Reaper Track
        T.Receive()
        T2 = r.Track(A) # This will recall the previously created Track with the same Address!
        # T2.Receive() # Not needed, T2 is T :-)
        Say("Tracks Created with the Same Address are the Same Objects:", T2 is T)
        Say("T2:", T2.Elements)