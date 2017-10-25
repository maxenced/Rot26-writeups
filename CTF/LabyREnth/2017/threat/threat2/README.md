So, at the time I started this challenge a hint has been given. It says that :

* There are 308 wildcard "?"'s within the answer (we already knew that)
* for a total of 298 byte matching hex-rule

Also the hint talks about function similarity. So likely we have to find a
function which exists in all binaries with lot of variations.

Also the hint uses bindiff and ida. I would like to avoid having to install ida, so let's try to solve it in antoher way.

TL;DR : grep & python FTW :)

# Main idea

So for each pro/epilogue, we will try to get all the block like '<opcode for push>[a-f0-9]\{592\}<opcode for pop>3c'.

Then, if we find at least one in each file, we will filter them with an algorithm like :

```python
for line in first_file.readlines():
  for file in all_files_but_first:
    for f_line in file.readlines():
      if different_char_count(line,f_line) > 308:
        skip line
      else:
        keep line
```

So with this, we will get n files (one per line of the first file) and in each
file all the lines from other files that have less than 308 different chars.

From this, we will be able to build a first version of yara rule. Everytime a
char is different in at least one line, just replace it by a '?'.

Then, if we have more than 308 ?, we will have to reduce the number by trying
to replace each of them with an hex char, as long as it matchs all the 56
samples.

# Find possible prologue / epilogue

So we will try to extract all functions with a similar prolog/epilog and
correct size. If we look at one of the smallest files
(64666128a96a6cf39f8ece9fe051db5c909d948d3c2f2f2983a9a51353308ae8) we have :

```
$ objdump -D 64666128a96a6cf39f8ece9fe051db5c909d948d3c2f2f2983a9a51353308ae8 |grep -B1 ret |grep pop |awk '{ print $2" "$3" "$4 }' |sort |uniq -c
      1 58 pop %eax
     38 59 pop %ecx
     13 5b pop %ebx
    210 5d pop %ebp
     18 5e pop %esi
      8 5f pop %edi
```

The more function there are, the more complex it will be to get the good yara
rule, so let's start with eax, then edi, ebcx,esi and ecx and ebp.

Corresponding opcode for push are :

```
$ objdump -D 64666128a96a6cf39f8ece9fe051db5c909d948d3c2f2f2983a9a51353308ae8 | grep 'push *%e'  |grep -v 'ds ' |awk '{ print $2" "$3" "$4 }' |sort -u |grep ^5
50 push %eax
51 push %ecx
52 push %edx
53 push %ebx
54 push %esp
55 push %ebp
56 push %esi
57 push %edi
```

## eax

So it starts with eax register. We extract all the code block of 596 hex chars long, starting with 50 and ending with 58c3:

```bash
$ for f in labyrenth/*; do echo $f; xxd -ps  $f |tr -d '\n' |grep -o '50[a-z0-9]\{590\}58c3' > ${f}.eax.hex  ;done
```

Basically, we dump each binary as hex, and grep the 596 chars which are of some interest.

It takes some time, so look at same time if at least one line is found :

```bash
$ wc -l labyrenth/*eax.hex
0 labyrenth/0b5ce1505ad29a8d89326e53745b5d0a43157462e0f0c3dbf6b2baa872ea936d.eax.hex
0 labyrenth/0b94a456e6fe41c7f31e5e43fd88f66f6d223db124163abedc56562be3e69a10.eax.hex
```

So no bloc found, you can cancel it and move to next opcode.

## edi

Same with 57/5f opcodes :

```bash
$ for f in labyrenth/*; do echo $f; xxd -ps  $f |tr -d '\n' |grep -o '57[a-z0-9]\{590\}5fc3' > ${f}.edi.hex; done
```

and same "issue" : no block found in first file. We can move on.

## ebx

Same again with 53/5b opcodes:

```bash
$ for f in labyrenth/*; do echo $f; xxd -ps  $f |tr -d '\n' |grep -o '53[a-z0-9]\{590\}5bc3' > ${f}.ebx.hex  ;done
```

This one looks much better, it has found exactly one block per file :

```bash
$ wc -l labyrenth/*ebx.hex
    1 labyrenth/0b5ce1505ad29a8d89326e53745b5d0a43157462e0f0c3dbf6b2baa872ea936d.ebx.hex
    1 labyrenth/0b94a456e6fe41c7f31e5e43fd88f66f6d223db124163abedc56562be3e69a10.ebx.hex
    1 labyrenth/10f419f90602e818727a8ce8fe03796ec0094528467942f6a7229477ee55902a.ebx.hex
    1 labyrenth/14fe68c477fa6c02fe1328dfefc93ded488aa31ad5765c7be339cb83b537587a.ebx.hex
    1 labyrenth/155fbef2536ef18fa0164f0ce3c40c3724122c0aef2246a1c8678489d50ec89e.ebx.hex
    1 labyrenth/1f0943c56d45ea07c7bd9dd245001aab6566afb64b78c5ebf1fdaebfdbe0e619.ebx.hex
    1 labyrenth/20abd8fa862d7f83a901218586d64111a00f146fac8e82479ebac967f924c3c0.ebx.hex
    1 labyrenth/2a5efc87bd878d9798aacc996d62f51936b6affcb9d5b1d631d7ff78ef5e9e19.ebx.hex
    1 labyrenth/2b6d9170a32b2b559e4fa93cc0c0898a21d5a304e48c616564479454ac85af59.ebx.hex
    1 labyrenth/2d298aeef216960c6162478ea11839d71337fe98c3b1bbcb48f3ba520b13a0e8.ebx.hex
    1 labyrenth/2d37480922e6fd894a4bd535190be297673ac7b89e6e36cf0543816a9e629898.ebx.hex
    1 labyrenth/32a78fe0db43d59b501fc2659cbecde64eec2f2d65f372519194e1e2ca3d0599.ebx.hex
    1 labyrenth/38ccc6847c5aa91c794d72f25597add06a609af9e69df1f69f2365320ca0ea6d.ebx.hex
    1 labyrenth/3926ebcba648af1f8df872f95a1ab1b3ae541605da8721b9b125fd01f4609b31.ebx.hex
    1 labyrenth/3ad8a5029df478c3edc22eaca6728db726b8a227346436efdd9391db47b3863b.ebx.hex
    1 labyrenth/3b957d02963f10c8443ceca0e954180e9be4af4b5c82e1fa9d9953eb008d08c5.ebx.hex
    1 labyrenth/3d6ea8b12778b6714648e5c33ee11f7cc720ccdc9803f713229b10ccef23e84c.ebx.hex
    1 labyrenth/466d8ec3f8c25e572f2a3e51d81273143fb57a108d51e2d0963f401d63cbd24e.ebx.hex
    1 labyrenth/46969095865baa3000dc306f28b2a0d15e447560bc45a9e00ad7b177b6589b13.ebx.hex
    1 labyrenth/47a17f8b554351797dab78b598416aa124805e97e3b764e10e822f561868123e.ebx.hex
    1 labyrenth/4ee643244b54538db0ca4d41d56f5b8194e27f9f06136251f817dcb1245033f0.ebx.hex
    1 labyrenth/64666128a96a6cf39f8ece9fe051db5c909d948d3c2f2f2983a9a51353308ae8.ebx.hex
    1 labyrenth/69ade5ee1c9f5cde6d0d8e328045e5bfdb75ccbb25a3f5473e1be8d09707b0f1.ebx.hex
    1 labyrenth/75a0fa788a3980dd83936ff499547e351d2ddc47a45bab8ca65844574a973897.ebx.hex
    1 labyrenth/795fb5b7529321234aec6c6d30a5418bd8dbaa664926762e8da163989faacc78.ebx.hex
    1 labyrenth/79d1c3c8d3fe59ded94c5892b199940332c045abb7acb5255e1ee5afb5e8195e.ebx.hex
    1 labyrenth/7c8caae3a3ee3517240a34d576beed197a27d7a8a8f18fa02c3f203417000bf9.ebx.hex
    1 labyrenth/7cf32159db855ebf5e3ed64130c7921e28433d731406ac7a4d3842580dcecb9f.ebx.hex
    1 labyrenth/7f63e65ab460ff8ad607ede5bedb9573263015ba81824c3896f5416969353dba.ebx.hex
    1 labyrenth/82821ea735d3d0463ab295a0dd1e64f6e8833ea418a8cc73f165541489d3b6e1.ebx.hex
    1 labyrenth/8b6cfd4a49e1e76421f327569f2445432d833b9187601d5269e24c8896aebc39.ebx.hex
    1 labyrenth/8e1769aa452950592bc4098eec7101f87e0382692eaf53bd63d7f273722c47ab.ebx.hex
    1 labyrenth/94484012cb187ad0eeddd99d42ed452717f59f70f3f26f80c25a9b6bbd6f7f0d.ebx.hex
    1 labyrenth/9879a8f439f9f3d13eff5a7be9c4a300f78182be967b304ecf0453b497755558.ebx.hex
    1 labyrenth/9ad76867220795ad167e1a6a0bce6744659eaf46f291594f7fc6d4f7d672a1ce.ebx.hex
    1 labyrenth/9d980b27abcfe05c0b7438bd8e3d4f970bdd62c6f7b6ea63bdcb85d036915433.ebx.hex
    1 labyrenth/a44545124bbd2bdf26d5808aba37add70f8e163ec80a786f1235d26881cb23a7.ebx.hex
    1 labyrenth/afd43c68938a8a77f7cd29e8f1d299eb5a8e29ca7be028815aa6f912cdaba639.ebx.hex
    1 labyrenth/baf77017268ad4ce1e38add11815ea337956ce081fe58762070c6bf19b45fede.ebx.hex
    1 labyrenth/bfc5fe7eedccfff4ea017963f165b33705e2a81e4beb4f19103973882df58c7b.ebx.hex
    1 labyrenth/c9006adac29f0f9b88927485e285a75b3a45e3e4cabc4bfe844999418e7acac4.ebx.hex
    1 labyrenth/c99b32b4bd6744311cdb357c8fa2210de6b79873f104a8f6268c2e60c606d330.ebx.hex
    1 labyrenth/ca1de4dc7c12262f4b9a98eddad0ba83c7603181fa0bcfa59cfdb22cfb5e1e3e.ebx.hex
    1 labyrenth/ca990312aa135c403cec4451cb1efd96d446c059bad5a11bc4368bd4cf940ee4.ebx.hex
    1 labyrenth/cc57de582a0cb1d6e0aa64c7cb69d8b6549745c4fe2e8547b4f4f14591a1e8fd.ebx.hex
    1 labyrenth/cf79f0874f35083abf04275e792fdf82b21ab0cf6d95aa4949ff23eea2a96ff7.ebx.hex
    1 labyrenth/d355ee7f9bc564f98f9cc3b667e4feaa8a34a934fdbd82755a50a473f0230691.ebx.hex
    1 labyrenth/d4322b061d829136ab87ad51e28e0f68cb098074c94c011fabded5d0111afad0.ebx.hex
    1 labyrenth/d4c47549f7814a09d360e243781918b6fc719949239ef72b9f66c246444757fc.ebx.hex
    1 labyrenth/de8d6ef64a8d9137834013f7263e9bdebb3be48f562af5679779376aaab0af5a.ebx.hex
    1 labyrenth/e683f76dd6d00e7c0053077b841e0e9d9b8df72cc9c194c188fdfbf17aa84fca.ebx.hex
    1 labyrenth/e701b4c7f45a71429d92d3127ea9cd38a8fcf2fb1a0b46c489cd784cff6a80a7.ebx.hex
    1 labyrenth/e806320dc92df9837ca01b78ab10a8d24eed3e3a94aad0a064c03088a5d40819.ebx.hex
    1 labyrenth/ef763faec48e5e29d63c38088b2fc3cebb5086bb805e6f3b020649c7bbbf8614.ebx.hex
    1 labyrenth/f05ee7e7259c85c5052dd01a18dbc123d2dedd7fe016aba7e5a59a18451e33dd.ebx.hex
    1 labyrenth/fa9b6d34a5295940d85b8a598902d0e0f26252ef705c9dadde3e473f3eb1ccdc.ebx.hex
   56 total
```

So just cross you finger and check they have at most 308 chars not in common.

# Check correlation

So the idea here is to check that each line have at most 308 chars not in common with the line from first file.
I wrote a small python script for this.

_Note_ : This script is unnecessarily complex as it has been written to handle
more than 1 line per file and get the one with most char in common. But still, it works :)

The script is here :

```python
#!/usr/bin/env python3
#coding: utf-8

import glob

def diffcount(a, b):
    """ Return the number of different chars between a and b
    """
    assert(len(a) == len(b))
    return sum ( a[i] != b[i] for i in range(len(a)) )

files = glob.glob("labyrenth/*.hex")
print("Working on %s files" % len(files))
reference = files[0]
files.remove(reference)

results=0
with open(reference,'r') as ref_file:
    for line in ref_file.readlines():
        print("My new reference is %s" % line)
        good=True
        with open("result_" + str(results) +".res", "w") as output:
			print("Create result file : %s" % "
            output.write(line)
            for f in files:
                if not good:
                    break
                with open(f,'r') as compare_file:
                    best_line = (309,'')
                    for compare_line in compare_file.readlines():
                        if len(compare_line.strip()) != 596:
                            break
                        if diffcount(compare_line, line) < best_line[0]:
                            best_line=(diffcount(compare_line, line), compare_line)
                    if best_line[0] == 309:
                        # nothing found
                        good=False
                        break
                    output.write(best_line[1])

        results += 1
```

And the result is :

```bash
$  ./find_correlation.py
Working on 56 files
My new reference is 53568b359c20011057682c240110ffd6681c2401108bf8ffd66810240110ffd66804240110ffd68b35f020011068f0230110578bd8ffd668e023011057a3907b0110ffd668d023011057a32c7d0110ffd668c023011057a3747b0110ffd668ac23011057a3a47c0110ffd6689823011057a3ac7c0110ffd6687c23011057a354780110ffd6686823011057a3287d0110ffd6685423011057a3787b0110ffd6684023011057a3847b0110ffd6683023011057a340780110ffd6681c23011053a3387d0110ffd6680423011053a3347d0110ffd668f822011057a3687b0110ffd668dc22011057a38c7b0110ffd668cc22011057a3247d0110ffd668bc220110a34c78011057ffd668b422011057a37c7b0110ffd668a022011057a3a87c0110ffd65f5ea3807b01105bc3

Create result file result_0.res
```

We can check the number of lines in this file :

```bash
$ wc -l result_0.res
56 result_0.res
```

Perfect ! All the lines from all the files have less than 308 chars not in common with the refence one.

Next step, try to create our yara rule :)

# Create rule

This part is simple. We compare the Nth char of every line. If they are not all equals, we put a "?". Else we keep the char.

Once again, python to the rescue :

```python
import sys

f=sys.argv[1]
lines=[]
res=''

with open(f,'r') as src:
    lines = src.readlines()

for i in range(0,len(lines[0])):
    comp = list(map(lambda x: x[i], lines)).count(lines[0][i])
    if comp < len(lines):
        res += '?'
    else:
        res += lines[0][i]

print(' '.join([res[i:i+2] for i in range(0,len(res),2)]))
print(res.count('?'))
```

And result :

```bash
$  ./generate_rule.py result_0.res
53 56 8b 35 ?? ?? ?? ?0 57 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 8b f8 ff d6 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 ff d6 8b 35 ?? ?? ?? ?0 68 ?? ?? ?? ?0 57 8b d8 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 a3 ?? ?? ?? ?0 57 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 5f 5e a3 ?? ?? ?? ?0 5b c3

308
```

w00t, 308 question marks ! Let's submit it :

# *PAN*

```bash
$ cat rule_test.yara

rule yara_challenge
{
        strings:
                 $yara_challenge = { 53 56 8b 35 ?? ?? ?? ?0 57 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 8b f8 ff d6 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 ff d6 8b 35 ?? ?? ?? ?0 68 ?? ?? ?? ?0 57 8b d8 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 a3 ?? ?? ?? ?0 57 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 5f 5e a3 ?? ?? ?? ?0 5b c3 }
        condition:
                 all of them
}
```

```bash
$ cat rule_test.yara| nc  52.42.81.161 8082
[...]
SUCCESS! KEY IS: PAN{AllByMyself}%
```
