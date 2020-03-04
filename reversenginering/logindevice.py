import socket
# UDP server 6602
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',6602))
print('UDP Server, port 6602')

# conn, addr = sock.accept()
# print(addr)
while True:
	data = b''
	addr = ('',0)
	sock.settimeout(60)
	try:
		data, addr = sock.recvfrom(1024)
	except socket.timeout:
		print('TimeOut')
	# data = conn.recv(1024)
	print('Client addr:', addr)
	if not data:
		pass
	else:
		print(data)
		data = b'$$dc0058,772,C100,0150008,,200211 221149,V101,200211 222403,0,1,2,#'
		sock.sendto(data, addr)

conn.close()

