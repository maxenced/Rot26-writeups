#!/usr/bin/python2

from flag import flag
from base64 import b64decode
from SocketServer import ThreadingTCPServer
from sys import argv
from binascii import hexlify, unhexlify
import SocketServer
import os

N = 8
MAX_TRIES = 1024
PAD = 64

welcome = "Welcome! :-)\n"
menu = "What would you like to do:\n\t1: supply encoded input,\n\t2: tell me my secret\n> "

def gen_secret():
    return os.urandom(N)

def crypt(s1, s2):
    return "".join(map(lambda c: chr(((ord(c[0])^ord(c[1]))+PAD)%256), zip(s1,s2)))

b64chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"
def decode(s, secret):
    enc = ""
    s = crypt(s, secret)
    
    for c in s:
        if c in b64chars:
            enc+=c

    if len(enc) % 4 == 1:
        enc = enc[:-1]

    while len(enc) % 4 != 0:
        enc+="="

    return b64decode(enc)

class B64Handler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.tries = 0
        self.secret = gen_secret()

    def handle(self):
        self.request.send(welcome)
        for i in range(MAX_TRIES):
            self.request.send("Round number: {}\n{}".format(i, menu))
            if self.request.recv(2)[0] == "1":
                self.request.send("What would you like me to decode?\n> ")
                answer = self.request.recv(len(self.secret))
                decoded = decode(answer, self.secret)
                self.request.send("Alright, here is your answer: {}\n".format(decoded))

            else:
                self.request.send("Alright, what is my secret (hex encoded)?\n> ")
                answer = self.request.recv(2*len(self.secret)+1).rstrip()
                if answer==hexlify(self.secret):
                    self.request.send("Well done, here is your flag: {}\n".format(flag))
                else:
                    self.request.send("This was not what I was looking for. :-(\n")
                break

        self.request.send("Bye!\n")

def main():
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    if len(argv) < 2:
        print("Usage: {} <PORT>".format(argv[0]))
    else:
        LOCAL_PORT = int(argv[1])
        s = SocketServer.ThreadingTCPServer(("", LOCAL_PORT), B64Handler)
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("shutting down")
            s.shutdown()
            s.socket.close()

if __name__ == "__main__":
    main()

