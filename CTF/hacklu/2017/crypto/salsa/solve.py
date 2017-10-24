#!/usr/bin/env python
#coding: utf-8

from pwn import *
from binascii import *
import salsa20
import json
import base64

r = remote('flatearth.fluxfingers.net',1721)
#r = remote('localhost',9999)

xor=lambda a,b: "".join(chr(ord(i) ^ ord(j)) for i,j in zip(a,b))

block_unknown=r.recv()
log.info("I have my block of %s chars" % (len(block_unknown)))

u=base64.b64encode("a" * int(128*0.75))
j_u=json.dumps({"cnt": 1, "data" : u })

r.sendline(base64.b64decode(u))
tobreak2=r.recv()
second_ks=xor(tobreak2, j_u)

t = xor(second_ks,block_unknown[1:])
log.warn("FLAG: %s "  % (base64.b64decode(json.loads("{" + t)['data'])))


