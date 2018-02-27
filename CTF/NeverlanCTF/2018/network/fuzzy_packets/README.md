Fuzzy Packets
=============

So, we just got a pcap file with some icmp traffic in it.

Looking at it with our favorite tool (Wireshark) we can notice that:

 * There is a bunch of request without associated answers
 * The is some icmp payload, just saying 'This is not the flag you are looking for'
 * Most of the requests are identical, except the code attribute which varies betwwen 0 and 1

Let's try to display those 0/1 and convert them to ascii :

```bash
$ tshark -r neverlan.pcapng  -T fields -e icmp.code   |xargs echo |tr -d ' ' | perl -lpe '$_=pack"B*",$_' |hexdump -C
00000000  66 5b 4c 5a 2c 56 70 df  1b af 37 39 06 ee 84 c7  |f[LZ,Vp...79....|
00000010  60 d9 24 31 b0 82 26 24  50 6c 4d e7 a7 a3 5f ca  |`.$1..&$PlM..._.|
00000020  9e 8b f0 c9 7c cc 24 dc  c0 83 6c 68 5b 1b 4d 2b  |....|.$...lh[.M+|
00000030  6d ac 6c ee 44 da 8c 56  14 eb 96 dd 3a de c2 52  |m.l.D..V....:..R|
00000040  ba 6f 0c af e4 7d 0a                              |.o...}.|
00000047
```

Well, just some garbage, but:

 * the first char is 'f'
 * the last char is '}'

Which looks like a 'flag{....}' string, doesn't it ? 

Looking again at the pcap we can see that 8 firsts and 8 lasts packets were requests, so try to only get icmp.code from them :

```bash
$ tshark -r neverlan.pcapng  -T fields -e icmp.code "icmp.type == 8"  |xargs echo |tr -d ' ' | perl -lpe '$_=pack"B*",$_'
flag{SayHi2@FuzzyNOP4Me-metacortex}
```

Here we go :)

