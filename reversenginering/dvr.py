import socket
import time

def get_current_dt():
    return datetime.datetime.today().strftime("%Y%m%d %H%M%S")
    pass

sock = socket.socket()
sock.bind(('0.0.0.0',6608))

sock.listen(1)

conn, addr = sock.accept()
print(addr)
try:
    while True:
        data = conn.recv(1024)
        if not data:
            pass
        else:
            print(addr)
            print(data)
            cmd = str(data).split(',')
            print(cmd)
            if cmd[2] == "V101":
                data = b'$$dc0058,772,C100,0150008,,200212 121149,V101,200211 222403,0,1,2,#'
                conn.send(data)
            elif cmd[2] == "V109":
                data = b'$$dc0030,4,C501,0150008,,200214 161054#'
                conn.send(data)
            elif cmd[2] == "V141":
                data = b'$$dc0066,2,C100,0150008,,200214 161044,V141,200214 212509,0,0,0,0,,,0,,0,,#'
                conn.send(data)
            print(data)
            #elif cmd[0] == "$$dc0175":
	#		ctrl1 = cmd[26]
	#		print('CTRL1:{}'.format(ctrl1))
	#		data = bytes('$$dc0068,2,C100,0150008,,200213 161321,V215,200213 161321,0,{}#'.format(ctrl1)) #,'utf-8')
	#		conn.send(data)
	#	elif cmd[0] == "$$dc0231":
	#		data = b'$$dc0060,14808,C100,0150008,,200213 162457,V101,200213 213921,0,1,2,#'
	#		conn.send(data)
# conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except:
    print('Socket terminate')
    conn.shutdown(socket.SHUT_RDWR)
conn.close()
#conn.shutdown(socket.SHUT_RDWR)
socket.close()
