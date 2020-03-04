import socket


sock = socket.socket()
sock.bind(('0.0.0.0',6631))

sock.listen(1)

conn, addr = sock.accept()
print(addr)
while True:
	data = conn.recv(1024)
	if not data:
		pass
	else:
		print(data)
		cmd = str(data).split(',')[0]
		print(cmd)
		#if cmd == "$$dc0229":
		#	data = b'$$dc0058,772,C100,0150008,,200212 121149,V101,200211 222403,0,1,2,#'
		#	conn.send(data)
		#elif cmd == "$$dc0248":
		#	data = b'$$dc0051,773,C7212,0150008,,200212 121149,195.133.201.27,6608,1#'
		#	conn.send(data)
conn.close()

