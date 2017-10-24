## Cyber Bullshit Cyber

Dans ce chall, on a un message chiffr√© et l'algo qui a servi √† le chiffrer.

Le message, pr√©sent dans le script python :

```python
""" Uncipher me : \x01@N\x02t\x1f60\xaf?\x1c\xf1\xadS\xe2\x9c\n\x97[\xaa\xf5\xd0\\\xd6\x86\xd7\x9e\xcaUr\\M\xc3Q\xae\x01e\x1e\xcbz\xbd\x8f\x89e^\xde'\xaa\xbf\xe4\x19\xe9\xef\x12r\xdb\xb0X\xff\\>\xa1\xad\x98\xa1+\xc6b\x11x\xb0#\xf2\xc3\xc6&\x0c\x87w\xfe\xf0\xd6)\xd8\xd8ox\xd1\xbaR\xf5V4\xab\xa7\x92
"""

L'algo utilis√© pour chiffrer est le suivant :

```python
def cipher(self, key, message):
     padded_message = self.pad_message(message)
     iv = os.urandom(32)
     ks = self.generate_ks(iv, key)
     blocks = self.split_to_blocks(padded_message)
     cipher_message = ""
     for block in blocks:
         cipher_block = self.xor(ks, block)
         ks = cipher_block
         cipher_message = "%s%s" % (cipher_message, cipher_block)

     return "%s%s" % (iv, cipher_message)
```

Donc:

	* on pad √† un multiple de 32
	* on g√©n√®re un iv
	* on g√©n√®re un digest via HMAC √† partir de l'iv et de la cl√©
	* on d√©coupe notre chaine en groupe de 32 chars
	* on XOR chaque bloc avec le digest

On remarque donc 2 choses :

	* Un seul IV est utilis√©
	* La cl√© (digest) est bas√©e sur l'IV et √©volue avec chaque bloc (principe du CBC)

Le message final contient en l'IV et le message avec son pad.

### R√©solution simple

La vuln√©rabilit√© principale du XOR est que l'op√©ration s'annule si elle est effectu√©e 2 fois.
On a une chaine qui fait exactement 96 chars, soit 3*32. Autrement dit :

 * Les 32 premiers chars sont l'IV
 * Les 32 suivants le d√©but du message
 * Les 32 derniers la fin du message + le padding


soient M1 et M2 les 2 parties du message en clair, et C1 et C2 les parties chiffr√©es, on a donc:

 * C1 = M1 ^ IV
 * C2 = M2 ^ C1

Et donc corrolaire :

 * M1 = C1 ^ IV
 * M2 = C2 ^ C1

On r√©cup√®re donc facilement le flag:

```python
#!/usr/bin/env python2

s="\x01@N\x02t\x1f60\xaf?\x1c\xf1\xadS\xe2\x9c\n\x97[\xaa\xf5\xd0\\\xd6\x86\xd7\x9e\xcaUr\\M\xc3Q\xae\x01e\x1e\xcbz\xbd\x8f\x89e^\xde'\xaa\xbf\xe4\x19\xe9\xef\x12r\xdb\xb0X\xff\\>\xa1\xad\x98\xa1+\xc6b\x11x\xb0#\xf2\xc3\xc6&\x0c\x87w\xfe\xf0\xd6)\xd8\xd8ox\xd1\xbaR\xf5V4\xab\xa7\x92"
iv=s[0:32]
msg=s[32:64]
pad=s[-32:]

r=''
def xor(x,y):
    res = ''
    for i in range(32):
        res += chr(ord(x[i]) ^ ord(y[i]))
    return res

print "%s" % (xor(pad,msg))
```

```bash
$ python test.py
6Ì≤èaÌ≤ñkÌ≥ìÌ≥±Ì≥ïJÌ≤∞Ì≤ïÌ≤îÌ≥≥Ì≤çÌ≥Ö6Ì≤µsBCÌ≥Ç.
M2 : bzhctf{YOLOCRYPTO2017}
```
