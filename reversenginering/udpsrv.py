#!/usr/bin/python
# -*- coding: utf-8 -*-

import SocketServer, threading, time
import datetime
import os
# converting for service 6608

ipServerStream = '127.0.0.1'

#def ssend_cmd(cmd1):
#    print('CLT >> "{}"'.format(cmd1))
#    message_b = bytes(cmd1,'utf-8')
#    sock.sendall(message_b)
#    recv_b = sock.recv(1024)
#    print('SRV >> "{}"'.format(recv_b))
#    return str(recv_b)

def get_current_dt():
    return datetime.datetime.today().strftime("%y%m%d %H%M%S")
    pass

def gw_comp_cmd(str1):
    len_cmd = str(len(str1)).zfill(4) # adding front zero 0001
    return '$$dc{}{}#'.format(len_cmd,str1)

# TCP Services
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
       self.server_address = server.server_address
       self.id_message = 100
       self.videoid = 0
       self.kill_received = False
       SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    # unpack messages
    def unpack_data_6608(self, data):
        message = ''
        # print('TCP:'.format(str(data)))
        arr_data = str(data).split(',')
        deviceid = arr_data[3]
        dev_dt = arr_data[5]
        if arr_data[2] == 'V101':
            # save to DB info this device
            #
            message = gw_comp_cmd(','+str(self.id_message)+',C100,'+deviceid+',,'+get_current_dt()+',V101,'+dev_dt+',0,1,2,')
            #self.message = self.message +1
            #message =  message + gw_comp_cmd(','+str(self.id_message)+',C508,'+deviceid+',,'+get_current_dt()+',57411032,1,0,1,0,'+ipServerStream+',6602')
            pass
        elif arr_data[2] == 'V109':
            # Query video stream C508  $$dc0063,29,C508,0150008,,200228 164317,46243800,1,0,1,0,127.0.0.1,6602#
            #message =  gw_comp_cmd(','+str(self.id_message)+',C508,'+deviceid+',,'+get_current_dt()+',57411032,1,0,1,0,'+ipServerStream+',6602')
            # C510 - video stream  $$dc0057,34,C510,0150008,,200228 164339,50930120,0,127.0.0.1,6602
            # C710 - video archive  $$dc0080,33,C701,0150008,,200228 164336,46214296,200228 000000,235959,3,0,127.0.0.1,6602#
            message =  gw_comp_cmd(','+str(self.id_message)+',C710,'+deviceid+',,'+get_current_dt()+',57411032,200228 000000,235959,3,0,'+ipServerStream+',6602')
        else:
            message = None # gw_comp_cmd(','+str(self.id_message)+',C'+str(self.id_message)+','+deviceid+',,'+get_current_dt()+','+arr_data[2]+','+dev_dt+',0,1,2,')

        self.id_message = self.id_message  + 1
        if message == None:
            return None
        else:
            return bytes(message)
        pass

    def handle(self):
        current_thread = threading.current_thread()
        print("TCP Server {}:".format(self.server_address))
        try:
            while not self.kill_received:
                response = b''
                data = self.request.recv(1024)
                if self.server_address[1] == 6608:
                    response = self.unpack_data_6608(data)
                    if not response == None:
                        print('SEND:{}'.format(response))
                        self.request.sendall(response)
                elif self.server_address[1] == 6602:
                    
                    arrData = bytes(data)
                    if os.path.isfile('/var/www/video'+str(self.videoid)+'.h264'):
                        print(type(arrData))
                        print('Adding to end of file!')
                        with open('/var/www/video'+str(self.videoid)+'.h264','ab') as f:
                            f.write(arrData)
                            #for ind in range(0,len(arrData)-1):
                            #    f.write(arrData)

                    else:
                        #if arrData[0] == '@':
                        #   print(data)
                        #else:
                        #   print(type(data))
                        #if not str(data[0]) == '@':
                        with open('/var/www/video'+str(self.videoid)+'.h264','wb') as f:
                            #for ind in range(0,len(arrData)-1):
                            f.write(arrData)
                    #if len(arrData) < 1024:
                    #    self.videoid = self.videoid + 1
                    print('TCP 6602 write len data {0} '.format(len(data)))
        except Exception as e:
            print(e.__class__)
            print("Error send data:{}".format(data))
            exit(0)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    deamon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
	#print('Start service TCP:{}'.format(server_address))
        self.servre_address1 = server_address
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

    pass



# UDPServices

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
       self.server_address = server.server_address
       SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        current_thread = threading.current_thread()
        print("UDP Server {}:".format(self.server_address))
        current_thread = threading.current_thread()
        response = ''
        try:
            data = self.request.recv(1024)
            print("{}: client: {}, write: {}".format(current_thread.name, self.client_address, data))
        except:
            print("UDPService {}: Error recv data ".format(self.client_address))
        try:
            self.request.sendto(response)
        except:
            print("Error send!!");


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):

    deamon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        #print('Start service UDP: {}'.format(server_address))
        self.server_address1 = server_address
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass)

    pass


def create_srv_tcp(port):
    print("Init TCP server:{}".format(port))
    server_t = ThreadedTCPServer(("0.0.0.0", port), ThreadedTCPRequestHandler)
    server_thr = threading.Thread(target=server_t.serve_forever)
    server_thr.daemon = True
    return server_thr

def create_srv_udp(port):
    print("Init UDP server:{}".format(port))
    server_t = ThreadedUDPServer(("0.0.0.0", port), ThreadedUDPRequestHandler)
    server_thr = threading.Thread(target=server_t.serve_forever)
    server_thr.daemon = True
    return server_thr


if __name__ == "__main__":
    # array all TCP ports
    # Port 7000 - jtt808
    listTCPPorts = [6602,6608] #[6608,6602,6603,6604,6605,6606,6607,6609,6610,6611,6612,6617,6618,6619,6620,6621,6622,6630,6631,6632,6633,6634,6635,7000]
    listUDPPorts = [6602,6608] #[6602,6603,6604,6605,6606,6607,6607,6608,6609,6610,6611,6612]
    server_arr = []

    # Create list all TCP servers
    for tcp_port in listTCPPorts:
    	server_arr.append( create_srv_tcp(tcp_port))
    # Create list all UDP servers
    for udp_port in listUDPPorts:
        server_arr.append( create_srv_udp(udp_port))


    try:
        for server_item in server_arr:
            server_item.start()

        print("Server started ")
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        for server_item in server_arr:
            server_item.kill_received = True
            # server_item.shutdown()
            # server_item.server_close()
        exit()
