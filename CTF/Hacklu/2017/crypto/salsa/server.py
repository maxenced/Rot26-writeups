import asyncore
import socket
import os
import base64
import json
import salsa20
from secret import FLAG

KEY = os.urandom(32)

class TCPHandler(asyncore.dispatcher_with_send):

    def __init__(self, socket):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self.Nonce = os.urandom(8)
        self.MsgCounter = 0
        self.sendMessage("Hello my dear friend, the flag is %s!" % FLAG)

    def sendMessage(self, data):
        text = base64.b64encode(data)
        for i in range(0, len(text), 128):
            msg = {"cnt" : self.MsgCounter, "data" : text[i: i+128]}
            msgtext = json.dumps(msg)
            encdata = salsa20.s20_crypt(KEY, self.Nonce, self.MsgCounter, msgtext)
            self.MsgCounter += 1
            self.send(encdata)


    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.sendMessage(data)

class TCPServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            handler = TCPHandler(sock)

server = TCPServer('0.0.0.0', 9999)
asyncore.loop()