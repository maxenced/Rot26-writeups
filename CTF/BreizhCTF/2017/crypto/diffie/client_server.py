from math import sqrt
from random import randint
import hashlib
import sys
import socket
from Crypto import Random
from Crypto.Cipher import AES

pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
unpad = lambda s : s[0:-ord(s[-1])]

def encrypt(message, key):
    message = pad(message)
    IV = Random.new().read(AES.block_size)
    aes= AES.new(key, AES.MODE_CBC, IV)
    return "%s%s" % (IV, aes.encrypt(message))

def decrypt(message, key):
    IV = message[:AES.block_size]
    aes = AES.new(key, AES.MODE_CBC, IV)
    return unpad(aes.decrypt(message[AES.block_size:]))

server = "0.0.0.0"
is_server = True
shared_secret = ''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        server = sys.argv[1]
        is_server = False

    shared = 65535
    private_key = randint(10**24,10**32)
    public_key = shared * private_key
    
    try:
        if is_server:
            print("Start server")
            s.bind((server, 31337))
            while True:
                s.listen(5)
                client, accept = s.accept()
                pub = client.recv(128)
                client.send(str(public_key))
                intermediate = long(pub) * private_key
                shared_secret = hashlib.sha256(str(intermediate).encode("utf-8")).digest()
                print("Key exchange completed")
                while True:
                    secret_message = client.recv(1024)
                    message = decrypt(secret_message, shared_secret)
                    print("<<< %s" % message)
                    message = raw_input(">>> ")
                    secret_message = encrypt(message, shared_secret)
                    client.send(secret_message)
        else:
            print("Connect to %s" % server)
            s.connect((server, 31337))
            s.send(str(public_key))
            while True:
                pub = s.recv(128)
                intermediate = long(pub) * private_key
                shared_secret = hashlib.sha256(str(intermediate).encode("utf-8")).digest()
                print("Key exchange completed")
                while True:
                    message = raw_input(">>> ")
                    secret_message = encrypt(message, shared_secret)
                    s.send(secret_message)
                    secret_message = s.recv(1024)
                    message = decrypt(secret_message, shared_secret)
                    print("<<< %s" % message)

    except:
        s.close()