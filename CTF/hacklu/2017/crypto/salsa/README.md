# Salsa

In this challenge we get the source code of some kind of online-encryption service.

When you connect to the socket, you get a piece of random data, and whenever
you write something to it, you get another piece of data back.

Looking at the `server.py` file we can see that this service encrypt what we send to it with Salsa20 algorithm.
Also, when you connect to it, the data you get is the flag, encrypted.

Some interesting facts :

```python
self.sendMessage("Hello my dear friend, the flag is %s!" % FLAG)
[...]
msg = {"cnt" : self.MsgCounter, "data" : text[i: i+128]}
```

So each text will be split in 128 bytes chunks, and each chunk will be put in some json, with the counter.
Given that the counter starts at 0, we know the beginning of the message :

```python
{"cnt": 0, "data": "SGVsbG8gbXkgZGVhciBmcmllbmQsIHRoZSBmbGFnIGlz"}
```

(`SGV...` behing base64 version of 'Hello my dear friend, the flag is')

Ok, so we have 66 known chars, not too bad.

## Crypto flaw

Let's look a bit more to it, we can see that key is initialized only once when the script is run:

```python
KEY = os.urandom(32)
```

and that, nonce is set only once per session:

```python
def __init__(self, socket):
	asyncore.dispatcher_with_send.__init__(self, socket)
	self.Nonce = os.urandom(8)
	self.MsgCounter = 0
```

And, finally, we notice that the counter is incremented only every 128 chars.

Key and Nonce reuse sound like a bad idea...

Looking at the salsa implementation, it looks good, but one part is interesting:

```python
def s20_crypt(key, nonce, si, data):
    key = [ord(c) for c in key]
    nonce = [ord(c) for c in nonce]

    n = [0] * 16

    for i in range(8):
        n[i] = nonce[i]

    if (si % 64) != 0:
        b0, b1, b2, b3 = s20_rev_littleendian(si / 64)
        n[8] = b0
        n[9] = b1
        n[10] = b2
        n[11] = b3

        keystream = s20_expand32(key, n)

    outp = ""
    for i, c in enumerate(data):
        if ((si+i) % 64) == 0:
            b0, b1, b2, b3 = s20_rev_littleendian((si+i) / 64)
            n[8] = b0
            n[9] = b1
            n[10] = b2
            n[11] = b3

            keystream = s20_expand32(key, n)
        outp += chr(ord(c) ^ keystream[(si+i) % 64])
```

So what happends when we arrive with our counter set to 0 ?

The keystream is generated from the key and `n`. `n` is a 16 bytes array, which contains nonce + 4 bytes.
These 4 bytes are set by `s20_rev_littleendian` function, which takes in parameters either either `si` or `si+i`.

When the function is call for the first time (with the flag message as data) we
have `si == 0` so `si % 64 == 0`, so only the second block is called. On first char, we have `si+i == 0`.
After the 64 first chars, we will have `si+i == 64`, so `s20_rev_littleendian`
will be called with either `0` or `1` as parameters.

So, the message is encrypted by chunks of 64 chars, with a keystream created from counter (aka 0) and char position.

## Exploit

We can already easily guess what the first keystream is. As it is a simple xor,
all we need to do is to xor the cipher we get with the known plain-text:

```python
known=json.dumps('{"cnt": 0, "data" :"SGVsbG8gbXkgZGVhciBmcmllbmQsIHRoZSBmbGFnIGlz"}')
# hexdump of data received when we connect
tofind=binascii.unhexlify("80c0d3be1f2edb1e142598ca5adec4c281d373b174715661aa8c767282a71ce33c62fe2a627ba0481647b8a2714c2e422775122e3ed776c2a81eb72c210a5bd5b733c25a97e6f8e708fac306c31a9bf805293c09f4737ff598c5cdad8867b4176e905ab886b2a3af46556452c41a8db255af6403b8bd3db9a18139651539063592744c771f111587266e648c2c3e")
[ord(x) for x in xor(tofind[:64],known)]
[162, 187, 143, 156, 124, 64, 175, 66, 54, 31, 184, 250, 118, 254, 152, 224, 229, 178, 7, 208, 40, 83, 118, 91, 246, 174, 37, 53, 212, 212, 126, 164, 4, 5, 156, 114, 9, 28, 250, 15, 64, 47, 219, 203, 51, 33, 77, 47, 75, 25, 112, 67, 111, 164, 63, 138, 250, 113, 237, 127, 99, 103, 57, 146]
```

So this is the first keystream. If you look values of `n[8]` to `n[11]`, you
will see that they equals `0` for the first keystream, andonly `n[8]` is set to
1 for the second block. Nothing more changes.
However, this is enough to get a totally diferent keystream. We may be able to
reverse algorithm to the point where `n` is used, then increment `n[8]`, but
seems way too complicated for now.

So, to guess the second keystream, we'd need to be able to call `s20_rev_littleendian` with 1 as parameter.
We know that the counter is incremented every 128 chars only. So if the flag
(including the 'Hello my dear ...' string) is less than 128 chars, the counter
will be set to 1 for the first message we will send.

It means that, for our first block of the first message we send, we will have `si == 1`, so first block will be called with :

```python
    b0, b1, b2, b3 = s20_rev_littleendian(si / 64)
```

As `si / 64` is 0 we wil get the same keystream

so `s20_rev_littleendian` will be called with 0, and then, 63 chars later, with
1. So we will get the same keystreams than used to encrypt flag!

Just to check we're right we patch the `salsa20.py` to print keystreams, run it locally, and connect then send some payload, and we see:
```python
# First keystream of flag
keystream : [27, 180, 157, 138, 61, 3, 177, 186, 121, 64, 10, 153, 75, 211, 85, 95, 34, 154, 150, 232, 85, 187, 124, 18, 42, 83, 128, 14, 88, 50, 75, 201, 225, 99, 176, 4, 144, 205, 10, 68, 7, 61, 10, 192, 44, 120, 174, 26, 99, 190, 59, 186, 205, 20, 230, 99, 140, 19, 72, 25, 91, 87, 32, 213]
# Second keystream of flag
keystream : [115, 51, 122, 133, 149, 167, 154, 74, 176, 179, 164, 36, 114, 82, 48, 53, 8, 241, 8, 101, 255, 70, 0, 35, 83, 66, 177, 101, 10, 207, 183, 159, 149, 206, 249, 63, 161, 241, 66, 119, 221, 136, 174, 254, 23, 168, 82, 195, 130, 142, 233, 17, 42, 235, 139, 84, 141, 87, 49, 234, 244, 41, 85, 206]
# Third keystream of flag, I put a long flag to test
keystream : [53, 46, 176, 228, 62, 164, 35, 10, 253, 71, 0, 182, 48, 210, 23, 237, 129, 68, 11, 228, 149, 130, 96, 50, 204, 142, 173, 202, 128, 84, 118, 74, 89, 178, 193, 24, 40, 191, 194, 54, 108, 193, 190, 243, 189, 15, 147, 202, 36, 33, 222, 208, 207, 111, 201, 32, 55, 222, 3, 185, 3, 19, 39, 125]
# First keystream of message we sent
keystream : [27, 180, 157, 138, 61, 3, 177, 186, 121, 64, 10, 153, 75, 211, 85, 95, 34, 154, 150, 232, 85, 187, 124, 18, 42, 83, 128, 14, 88, 50, 75, 201, 225, 99, 176, 4, 144, 205, 10, 68, 7, 61, 10, 192, 44, 120, 174, 26, 99, 190, 59, 186, 205, 20, 230, 99, 140, 19, 72, 25, 91, 87, 32, 213]
# 2nd keystream of message we sent
keystream : [115, 51, 122, 133, 149, 167, 154, 74, 176, 179, 164, 36, 114, 82, 48, 53, 8, 241, 8, 101, 255, 70, 0, 35, 83, 66, 177, 101, 10, 207, 183, 159, 149, 206, 249, 63, 161, 241, 66, 119, 221, 136, 174, 254, 23, 168, 82, 195, 130, 142, 233, 17, 42, 235, 139, 84, 141, 87, 49, 234, 244, 41, 85, 206]
```

Perfect ! However, if you compute your keystream based on the plaintext you submitted on client side you will get :

```python
keystream : [180, 157, 138, 61, 3, 177, 186, 121, 64, 10, 153, 75, 211, 85, 95, 34, 154, 150, 232, 85, 187, 124, 18, 42, 83, 128, 14, 88, 50, 75, 201, 225, 99, 176, 4, 144, 205, 10, 68, 7, 61, 10, 192, 44, 120, 174, 26, 99, 190, 59, 186, 205, 20, 230, 99, 140, 19, 72, 25, 91, 87, 32, 213, 115]
```

You will notice that the first char is gone. This is becaus of :

```python
	outp += chr(ord(c) ^ keystream[(si+i) % 64])
```

So because `si = 1`, the keystream is shifted by one. We don't really care as we already know first char of the message ('{').

So all we finally need to do is to send a message whose base64 is 128 chars
long , get the result, xor result with message (including the json part), and
we'll get our full keystream!

Getting a 128 chars base64 string is easy, just encode a 128*0.75 chars string:

```python
len(base64.b64encode("a"*int(128*0.75)))
128
```

Then send it, get the result, xor it, and finally xor with cipher text starting at first char :

```python
u=base64.b64encode("a" * int(128*0.75))
j_u=json.dumps({"cnt": 1, "data" : u })
r.sendline(base64.b64decode(u))
tobreak2=r.recv()
second_ks=xor(tobreak2, j_u)
t = xor(second_ks,block_unknown[1:])
log.warn("FLAG: %s "  % (base64.b64decode(json.loads("{" + t)['data'])))
```

And here you go :

```python
$  ./solve.py
[+] Opening connection to flatearth.fluxfingers.net on port 1721: Done
[*] I have my block of 142 chars
[!] FLAG: Hello my dear friend, the flag is FLAG{CRYPTO_IS_EASY_TO_BREAK_IF_YOU_ARE_USING_IT_WRONG}!
[*] Closed connection to flatearth.fluxfingers.net port 1721
```

