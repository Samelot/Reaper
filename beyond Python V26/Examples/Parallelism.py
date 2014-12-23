import beyond.Reaper
import beyond.Screen


@ProgramStart
class Main(Screen):

	def Setup(o, e):

		e.Title("Parallelism")

		e.Text("Parallelism")
		e.Font("Helvetica 40 italic")
		e.Color("Dark Orange")
		e.Padding(20)

		with e.HorizontalCenter():
			e.Padding(20)

			e.Button("StartWorkerScreen", "Start New Worker")
			e.Button("StartWorker", "Start New Worker (No Screen)")
		
		e.Text("Received Progress:")	
		e.TextEditor("ProgressLog")
		e.Size(200, 400)
		e.Stretch()


	def ReceiveProgress(o, Worker, Progress):
		# All safe called from another Parallel or Screen (Thread), call will be automatically message queued
		o.ProgressLog.Insert("Worker: " + str(id(Worker)) + ", Progress: " + str(Progress) + "\n")



	def StartWorker(o):
		class Worker(Parallel):
			def Start(o):
				for i in range(10):
					for b in range(10000000): Busy = b * b
					o.Parent.ReceiveProgress(o, i)
		Worker(Parent = o)



	def StartWorkerScreen(o):
		W = o.WorkerScreen(Parent = o)
		W.Work() # This is safe too.  All Property and Method accesses between Parallels or Screens are automatically message queued

	class WorkerScreen(Screen):

		def Setup(o, e):
			e.Title("Parallel Worker " + str(id(o)))

			e.Text("Progress", "Ready")
			e.Font("Helvetica 40")
			e.Color("Dark Green")
			e.Padding(20)
	
		def Work(o):
			for i in range(10):
				o.Progress = "Working: " + str(i)
				o.Parent.ReceiveProgress(o, i)
				for b in range(10000000): Busy = b * b
				o.Wait(.001) # Allows to Process InputEnd (Window Closing)
				if not o.Visible: break

		def InputEnd(o):
			o.Visible = False