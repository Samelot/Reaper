import beyond.Reaper.Direct
import beyond.Reaper.Settings
import beyond.Network


try:

	with beyond.Network.Client(beyond.Reaper.Settings.External_Program_Address) as Client:

		Active = True
		while Active:

			L = Client.Receive()

			try:
				exec(L[0])
			except Exception as E:
				import traceback
				E.Traceback = traceback.extract_tb(E.__traceback__)
				L = E

			Client.Send(L)
			
except Exception as E: Say(E)