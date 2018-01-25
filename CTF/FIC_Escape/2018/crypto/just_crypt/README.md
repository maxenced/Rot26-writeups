# Just Crypt

In this challenge, we got the following base64 :

```
HQ1BFi0TZjw/JjlPOhAnEwd1LmQ2DiliICk4GloFLzgxB0EDZRsnJnAmPwBtCyMIDjADZDUAejEnJ0A1Pi1mJjFDFQ0pEmY9I3E4CW0QKxJCOQ4iJGUTLGIyIhFwJScgMEMOBGUFMyo9MCUGIx0xa2gGCGQ2CnoxIy8mETRpMz50Fw5CMR4jaCMkOWUZES4NQiICZCcALywmZj4cNWk1KzVDDgRlETQtNT9dLiMcYhYHdQstNwo+YiAjJBExPS5uIAsEQjIXMC0jWx4BbRc3E0IsAigtAC1iMTMoGTE7LyAxaWs1IFYnJDxxOwY7HWIIDHUGZDgKNi4tMWoHJSsrLyYKDwdPLyMkPD4gTz4NIAwDJw4qJEN6OycqJhsnaTU7Ng4AECwYI0IHNHcOIRRiDQsjAmQoAXojYj8vGDwmMW4nFgMPJAQvJjVbDgohFC0WQiYSJiwOKCssI2ZUKSwqIjsUQREwFCspIjg5CkdyAw8GdQgxM088MCsjJBAjaSc8MUMADilWKSZwMzgOPxxILAM7HmQsACgnYiksVCQhIyN0DwgUIFYoLSgldwsiFzBrIzsDZDUHP2IgJyQQcCsjKT0NEkIxGWY4PDAuZUcqF1Q2BjIOFQpqJgoeeyI2KncYPjobLz8sAHEFM2ZWCCIVLxswPwZxN2slNSUmTDgvF3NpaWs1IFYnJDxxOwY7HWIIDHUGZDgKNi4tMWoHJSsrLyYKDwdPLyMkPD4gTz4NIAwDJw4qJEN6OycqJhsnaTU7Ng4AECwYI0IHNHcOIRRiDQsjAmQoAXojYj8vGDwmMW4nFgMPJAQvJjVbDgohFC0WQiYSJiwOKCssI2ZUKSwqIjsUQREwFCspIjg5CkdyBBQOOUc3MQo/JmIvPlQ5OmpuBwQVTGR8BT0kcSMHKFghAAA5AmhhCygtMmY+HDVpJS82DwRDTzc/LXxxJAY/VGIAGzBGTgIOKjYjLyRYcConPiACCAxkfEwJI3EgCm0UKxcHdQZkLQY8J2IpLFQ1KDUrdEsgQikfIC1wPjFPKBkxBEtfIjIkHSMtLCNqGzZpMz10SyQUIAQ/Jz40dwArWDcSS3UPJTJPOy4uZj0RcCcjKzBDSSokBWYpPD13GChYLAQHMU5OEgQjYi0gahY8PCNufDAKG2UZIGgyPSIKZFgjDwZ1FCEgTzUkYiE4ETUnZmYHBgBCKhBmLyI0MgFkcgsPQjoSNmEWPy4uKT1UeAAobjsWE0I8EyokPyZ+Tz4NIAwDJw4qJE9yETckJxUiICgreEMJA2lWLil5W104KFgjDQ51Cy03CnorLGYrVCksKiI7FEERMBQrKSI4OQpHIScNDjoQZDIaOC8jNCMaNWVmNzEPDQ0yVjU9Mjw2HSQWJ2s1MEclLQN6LiswL1Q5J2YvdBoEDikZMWgjJDUCLAorDwdfPiEtAzU1YjU/Fj0oNCc6Bk1CPBMqJD8mdxw4Gi8AEDwJIUs4P2IjKiZUPCAwK3QKD0IkVj8tPD04GG0LNwMPNBUtLwpQGycqJhsnaTU7Ng4AECwYI2RwKDIDIRc1QREgBSkgHTMsJ0wdEXAoKiJ0DwgUIFYvJnAwdxYoFC4OFXUUMSMCOzArKC9+CSwqIjsUQREwFCspIjg5CmFYOwQOOQgzYRwvIC8nOB0+LGZE
```

And some information saying it is a simple xor of some english text. So all we had to do was to find the key.

We do this using our Kasiski elimination tools, and get : 

```bash
$ base64 -d xor_analysis.txt > xor_analysis.raw && ./xorlength.py xor_analysis.raw
[*] Finding most probable key lengths.
[+] Finding best length : : 32 (f = 70)
 1  |  13 |===
 2  |  16 |====
 3  |  11 |==
 4  |  18 |====
 5  |  11 |==
 6  |  14 |===
 7  |  13 |===
 8  |  15 |===
 9  |  14 |===
 10 |  21 |=====
 11 |  16 |====
 12 |  18 |====
 13 |  22 |=====
 14 |  17 |====
 15 |  22 |=====
 16 |  13 |===
 17 |   9 |==
 18 |  10 |==
 19 |  15 |===
 20 |  15 |===
 21 |   8 |==
 22 |  11 |==
 23 |   5 |=
 24 |  15 |===
 25 |   7 |=
 26 |  11 |==
 27 |   9 |==
 28 |  11 |==
 29 |   7 |=
 30 |  13 |===
 31 |  13 |===
 32 |  70 |=================
 33 |  13 |===
 34 |  28 |=======
 35 |  13 |===
 36 |  12 |===
 37 |  12 |===
 38 |  18 |====
 39 |   7 |=
 40 |  11 |==
 41 |   9 |==
 42 |  21 |=====
 43 |  13 |===
 44 |  10 |==
 45 |  16 |====
 46 |  19 |====
 47 |  14 |===
```

So looks like key length is 32.

We can now try to bruteforce it.

```bash
$ xortool -c ' '  -l 32 xor_analysis.raw
108 possible key(s) of length 32:
Tcab\x00v\x03\x04\x1cQW*\x014B-bU"D\x04*ZBB\x03\x06tPIFN
Tcab\x00v\x03\x04\x1cQW*\x014B-bU"D\x04*ZBB\x03\x06tPI\nN
Tcab\x00v\x03\x04\x1cQW*\x014B-bU"D\x04*ZBB\x03\x06tPI\x15N
Tcab\x00v\x03\x04\x1cQW*\x014B-bU"D\x04*ZBB\x03\x06t\x15IFN
Tcab\x00v\x03\x04\x1cQW*\x014B-bU"D\x04*ZBB\x03\x06t\x15I\nN
...
Found 108 plaintexts with 95.0%+ printable characters
See files filename-key.csv, filename-char_used-perc_printable.csv
```

Not to bad. Sadly none of them are clear plaintext, but we can see many interesting words, like 'yellow', 'submarine', etc ...
Sounds like Beatles song, doesn't it ? 

Now we know what we want to find, that's quiet easy to run a crible attack.

Using our favorit tool for this, we find the key `54 63 61 62 45 76 46 48 50 51 57 6F 4D 78 42 61 62 55 67 44 41 6F 5A 42 42 46 4A 74 50 49 46 4E` and so the plain text:

```
In the town where I was born~Liv
ed a man who sailed to sea~And h
e told us of his life~In the lan
d of submarines~~So we sailed up
 to the sun~Till we found the se
a of green~And we lived beneath
the waves~In our yellow submarin
e~~We all live in a yellow subma
rine~Yellow submarine, yellow su
bmarine~We all live in a yellow
submarine~Yellow submarine, yell
ow submarine~~And our friends ar
e all on board~Many more of them
 live next door~And the band beg
ins to play~~RU5TSUJTe0dHX1Vfc1V
jYzMzZF9Ub19EZWNyeXB0X1gwcl8hfQ=
=~~We all live in a yellow subma
rine~Yellow submarine, yellow su
bmarine~We all live in a yellow
submarine~Yellow submarine, yell
ow submarine~~Full speed it is,
Sgt.!~Cut the cable, drop the ca
ble!~Aye, sir, aye!~Captain, cap
tain!~~As we live a life of ease
 (A life of ease)~Everyone of us
 (Everyone of us) has all we nee
d (Has all we need)~Sky of blue
(Sky of blue) and sea of green (
Sea of green)~In our yellow (In
our yellow) submarine (Submarine
, ha, ha)~~We all live in a yell
ow submarine~Yellow submarine, y
ellow submarine~We all live in a
 yellow submarine~Yellow submari
ne, yellow submarine~We all live
 in a yellow submarine~Yellow su
bmarine, yellow submarine~We all
 live in a yellow submarine~Yell
ow submarine, yellow submarine ~
```

And so the flag was the base64 in the midle of the text `ENSIBS{GG_U_sUcc33d_To_Decrypt_X0r_!}`.
