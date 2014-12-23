import beyond
import socket, struct, pickle, io


PacketSize = 1024
TimeOut = 10


class ServerSingle:

	def __init__(o, Address):
		try:
			S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			S.bind(Address)
			S.listen(5)
			S.settimeout(TimeOut)
			S2, A = S.accept()
			o.Connection = Connection(S2, A)
		except:
			raise
		finally:
			S.close()
			
	def Send(o, D):
		o.Connection.Send(D)
		
	def Receive(o):
		return o.Connection.Receive()
	
	def End(o):
		o.Connection.End()

		
	
class Client():
		
	def __init__(o, Address):
		S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		S.settimeout(TimeOut)
		S.connect(Address)
		o.Connection = Connection(S, Address)
		
	def Send(o, D):
		o.Connection.Send(D)
		
	def Receive(o):
		return o.Connection.Receive()

	def End(o):	
		o.Connection.End()
	
	def __enter__(o):
		return o
	
	def __exit__(o, ExceptionType, Exception, Traceback):
		o.End()

		
	
class Connection:
	
	def __init__(o, Socket, Address):
		o.Socket = Socket
		o.Address = Address
	

	def Send(o, D):
	
		o.Socket.settimeout(TimeOut)
	
		B = io.BytesIO()
		B.seek(4)
		pickle.dump(D, B, pickle.HIGHEST_PROTOCOL)
		Size = B.tell()
		B.seek(0)
		B.write(struct.pack("<I", Size))

		B.seek(0)
		
		i = 0
		while i < Size:
			i2 = i + PacketSize
			if i2 > Size: i2 = Size
			o.Socket.send(B.read(i2 - i))
			i = i2
		
		B.close()
		
	
	def Receive(o):
	
		o.Socket.settimeout(TimeOut)
	
		B = io.BytesIO()
		
		B.write(o.Socket.recv(PacketSize))
		i = B.tell()
		if i <= 4:
			B.close()
			return None
		
		B.seek(0)
		Size = struct.unpack("<I", B.read(4))[0]
		B.seek(i)
		
		while i < Size:
			B.write(o.Socket.recv(PacketSize))
			i = B.tell()
				
		B.seek(4)
		D = pickle.load(B)

		B.close()

		return D
	
	
	def End(o):
		o.Socket.close()