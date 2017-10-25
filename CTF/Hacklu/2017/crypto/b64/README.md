# B64

So here we have a source code. Quickly looking at it, we can see that it get our input, xor it with the secret then pad it.
Then, for each char, if the ASCII value match a base64 character, we keep it, else we drop it.
Finally, the base64 generated value is padded , decoded, and the value is sent back to the client.

```python
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
```

Also, note that if the length of encoded value contains only one char, the answer is emptied.

So, we basically need to bruteforce the secret. The issue is that you need to
be sure that all your chars are valid (so that, basically, if you send N chars,
you must get 0.75*N in result).

We wil bruteforce the first 4 ones, then once we get them, the 4 last chars. Final script :

```python
#!/usr/bin/env python3
#coding: utf-8

from pwn import *
from binascii import *
import base64 as b64
import time
import random

x = ''
result = ''
hexresult = ''
tosend=''
done_iter=0
run=1
done=False
while not done:
    try:
        r=remote('flatearth.fluxfingers.net',1718)
        log.warn("Run number %s" % run)
        run += 1
        for z in range(0,8,4):
            ok = False
            progress = log.progress('bruteforce chars %s to %s' % (z,z+3))
            for i in range(0,1025-done_iter):
                i1 = random.randint(0,127)
                i2 = random.randint(0,127)
                i3 = random.randint(0,127)
                i4 = random.randint(0,127)
                c1 = chr(i1)
                c2 = chr(i2)
                c3 = chr(i3)
                c4 = chr(i4)
                r.recvline_contains('tell me')
                r.sendline(b"1")
                r.recvline_contains('to decode')

                progress.status("[Iter %s] Send : %s %s %s %s %s" % (i + done_iter, tosend , i1 ,i2, i3 ,i4))
                r.send(tosend + c1 + c2 +c3 +c4)
                x = r.recvline().strip()

                x = x.split(b'\n')[0].split(b':')[1][1:]
                bx = b64.b64encode(x)

                if (len(tosend) ==0 and len(x) == 3) or (len(tosend) > 0 and len(x) == 6):
                    a = bx[0+z]
                    b = bx[1+z]
                    c = bx[2+z]
                    d = bx[3+z]

                    progress.success('Found some chars after %s iterations' % i)
                    flag_char_1="%02x" % (((a - 64) % 256) ^ i1)
                    flag_char_2="%02x" % (((b - 64) % 256) ^ i2)
                    flag_char_3="%02x" % (((c - 64) % 256) ^ i3)
                    flag_char_4="%02x" % (((d - 64) % 256) ^ i4)
                    log.info("chr(%s),  char are (%s,%s,%s,%s)" % (i,flag_char_1, flag_char_2, flag_char_3, flag_char_4))
                    result += flag_char_1 + flag_char_2  + flag_char_3 + flag_char_4
                    tosend += c1 + c2 + c3 + c4
                    log.warn("Result : %s " % (result))
                    time.sleep(2)
                    ok=True
                if i == 1023-done_iter:
                    log.error("Did not find any value after 1024 tests, try again with new flag")
                    break
                if ok:
                    print("Result is %s long" % len(result))
                    if len(result) == 16:
                        done = True
                    done_iter = i
                    break
    except EOFError:
        log.warn('Got EOFError (after 1023 tests ? ), retrying')
        continue
log.warn("Your flag is %s" % (result))
if ok:
    r.interactive()

```

It does not always works, as we get 4 randint (< 127 so that we don't mess with unicode encoding etc ...).
Still, after 2 or 3 tries :

```python
 ./bf.py
[+] Opening connection to flatearth.fluxfingers.net on port 1718: Done
[!] Run number 1
[+] bruteforce chars 0 to 3: Found some chars after 415 iterations
[*] chr(415),  char are (b1,2f,73,d3)
[!] Result : b12f73d3
Result is 8 long
[+] bruteforce chars 4 to 7: Found some chars after 319 iterations
[*] chr(319),  char are (7f,5f,ea,a4)
[!] Result : b12f73d37f5feaa4
Result is 16 long
[!] Your flag is b12f73d37f5feaa4
[*] Switching to interactive mode
Round number: 736
What would you like to do:
    1: supply encoded input,
    2: tell me my secret
> $ 2
Alright, what is my secret (hex encoded)?
> $ b12f73d37f5feaa4
Well done, here is your flag: flag{7h3_b35t_w4y_of_h1ding_s3cr3t5_the_w0r1d_h4s_ev3r_seen_period!}
Bye!
[*] Got EOF while reading in interactive
```

Could be nicer, but it worked :)
