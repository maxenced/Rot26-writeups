Here we get a doc file with some uninteresting text ... and a macro. Let the fun begin !

# Extract first macro

```shell
$ olevba MarsSpider_Contract.doc > MarsSpider_Contract.macros.vbs
```

We get ~ 360 lines of VBS macro, including the creation of a rise.txt file with a big base64 payload. Let's look at it:


```shell
$ grep 'cGlsbHM =' MarsSpider_Contract.macros.vbs |cut -d '"' -f 2 |tr -d '\n' |base64 -d > rise.txt.raw
```

Looks like garbage, try a quick xor :

```shell
$ xortool -b  rise.txt.raw
Key-length can be 3*n
256 possible key(s) of length 15:
wtm`avwbvkiievw
vula`wvcwjhhdwv
uvobctu`tikkgtu
twncbutauhjjfut
spidersfrommars
```

last one looks nice :)

```shell
$ xortool-xor -r spidersfrommars -f rise.txt.raw
```

not so good, especially upper and lowercase seems to be mixed. Try :

```shell
$ xortool-xor -r SPIDERSFROMMARS -f rise.txt.raw > rise.vbs
```

much better !

rise.vbs seems to contain a powershell part, split it in another file :

```shell
$ head -2 rise.vbs > rise.ps
```

and the VBS part seems to be called "ziggy.vbs", so :

```shell
$ tail +3  rise.vbs | sed 's/.*ziggy.vbs//'  > ziggy.vbs
```

Also, it is a windows based file so :

```shell
$ file ziggy.vbs
ziggy.vbs: ASCII text, with very long lines, with CRLF, LF line terminators
$ dos2unix ziggy.vbs
file cGlsbHM.ps
cGlsbHM.ps: ASCII text, with very long lines, with CRLF line terminators
```

# Solve PowerShell

First things first, we have a quick look on powershell file. Cleaning it a bit,
we can see there are lots of 'if' condition which append some stuff to a `$s`
string and, from time to time, a call to `jaREth` function with `$s` in
parameter.

Reading the beginning of the code we see this :

```powershell
$bowielyric=IEX("{1}{3}{11}{9}{8} {2}{4}{7}{5}{0}{6}{10}"-f")","(","Win32","Get","_","System",".","Computer","Object","Wmi","Domain","-");
```

which is just a call to `(Get-WmiObject Win32_ComputerSystem).Domain`, which gets current domain.

Then, 4 variables are set from 3 domain's chars :

```powershell
$z=([Int](((2016-[Int]$bowielyric[1])*2)/70-47));
$i=([Int](([Int]$bowielyric[3]+1983)/420-1));
$g=([Int](((1970/[Int]$bowielyric[5])*9)-207));
$y=([Int](([Int]$bowielyric[5]*1969)/(278/2)/(200)-5));
```

And then all the `if` stuff uses these 4 variables to create numbers that are then hex-encoded by calling `jaREth`.
At the end, the hex string is decoded and executed.

So all we have to do is to bruteforce the 3 chars value. As it is a domain, just try with uppercase chars first (by convention).
So just put all this stuff inside 3 for loop and print the result at the end :

```powershell
For ($aa=65; $aa -le 90; $aa++) {
	For ($bb=65; $bb -le 90; $bb++) {
		For ($cc=65; $cc -le 90; $cc++) {
			$z = ([Int](((2016 - $aa) * 2) / 70 -47));
			$i = ([Int](($bb + 1983) / 420 -1));
			$g = ([Int](((1970 / $cc) * 9) -207));
			$y = ([Int](($cc * 1969) / (278 / 2) / (200) -5));

			# All the if stuff untouched

			($bowiesong -split '(..)') | % {
				[Convert]::ToInt32($_, 16)
			} | % {
				[Convert]::ToChar($_)
			} | % {
				$bowiealbum += ($_)
			}; # & ("{0}{2}{1}" -f$bowiealbum[4], "x", $bowiealbum[-4]) ($bowiealbum) &

			Write-Host $bowiealbum
		}
	}
}
```

just run it and look for the result :

```shell
$ powershell rise.ps
D´DdôddiFBFOFOFÔdFOFDÔ$´$´BFDdDFOFFFd$dôdômFDdôdDd`FBF`FBFÔdB$$FIDBBBÔ$$ B$$-BFBD B$BÔ$$$d BBBD-BD B$BBBÔ$$ B B-B$d BD BÔ$d)B BFBÔ)BBB BD-B B$$$BÔ$B BBB-BD B BD-BFBFB$BD-BD B$$)BÔ$BFB$$ BBBÔ$$Dd$dFBBBB$´BFÔdFd$-DFFFDdôdMFOFFB$$FFdôdFOFFFBBdôdddFBD$iFDmFÔ$
[...]
```

and after some time, you will see :

```powershell
[Environment]::SetEnvironmentVariable("HWID","093-75115-37124-50142-30110-87150-78116-83115-81124-51121-50114-67145-51139-47130","User");Clear-EventLog "Windows PowerShell"
```

Ok, so it only exports a HWID variable. Ready for next step !

# Ziggy VBS

So here we have an obfuscated VBS file. Appart the name mess, we can notice
there are lot of arithmetic stuff like `&H1ed-703+1hd3`, which does not help to
understand.  Let's fix that first:

```shell
$ grep -o '([0-9+-]*&H[^)]\+)' ziggy.vbs | while read line; do echo -n "$line : "; echo $line | sed 's/&H/0x/g' | python -c 'import sys
; print(eval(sys.stdin.read()))'  ;done
(&H36-197+&H92) : 3
(&H3c8-1128+&Ha0) : 0
(&H132-1082+&H309) : 1
(&H1ed-703+&Hd3) : 1
(&Hf5-553+&H138) : 4
```

We see lot of very small values. Let's sed everything :

```shell
$ grep -o '([0-9+-]*&H[^)]\+)' ziggy.vbs | while read line; do echo -n "sed -i \"s/$line/"; echo $line | sed  's/&H/0x/g' | python -c 'import sys; print("("+ str(eval(sys.stdin.read())) + ")/g\" ziggy.vbs")'  ;done | shell
```

Much better, but still the name obfuscation to solve.
After some cleaning/ordering we get this file :

```visualbasic
' Check some stuff in registry and returns either 0 or 1
registry_user_software_check_result = registry_user_software_check
date_now = now

' Get data in MOVDATA register key
' it was stored in MarsSpider_Contract macro and is composed of a date + a string of ascii value
set shell_object = createobject("Wscript.Shell")
movdata = shell_object.RegRead("HKEY_CURRENT_USER\Volatile Environment\MOVDATA")

' Chosse either 'TheDarkCrystal!' or 'WhereDidTobyGo?' based on registry check
if registry_user_software_check_result = (1) then
    func3_result = func3("VGhlRGFya0NyeXN0YWwh") ' TheDarkCrystal!
else
    func3_result = func3("V2hlcmVEaWRUb2J5R28/") ' WhereDidTobyGo?
end if

' Get date/time part from the movdata
movdata_datestr = mid(movdata,(1),(21))
movdata_date = CDate(movdata_datestr)

' Check if it is less than 30s from now
' likely some anti debug technique, so correct value should be func2(movdata)
if datediff("s",movdata_date,date_now) < (30) then
    func2_result = func2(movdata)
else
    func2_result = func2(StrReverse(movdata))
end if

' Open main doc file
' and extract a subsection of 2156 bytes
set fs_object=CreateObject("Scripting.FileSystemObject")
y_marsspider_path="Y:\MarsSpider_Contract.doc"
set y_marsspider_file = fs_object.GetFile(y_marsspider_path)

with y_marsspider_file.OpenAsTextStream()
    y_marsspider_content = .Read(y_marsspider_file.Size)
    .Close
end with
marsspider_subfile = mid(y_marsspider_content,(269217),(2156))

' Decrypt the content
cryptofunc_res = cryptofunc(marsspider_subfile)

' Create a bat file and store the decrypted content
set fs_object=CreateObject("Scripting.FileSystemObject")
y_594f54_bat="Y:\594f54.bat"
set y_marsspider_file = fs_object.CreateTextFile(y_594f54_bat,True)
y_marsspider_file.Write(cryptofunc_res)
y_marsspider_file.Close

' and run this bat file
set y_marsspider_file = fs_object.GetFile(y_594f54_bat)
y_marsspider_file.attributes=(2)

CreateObject("WScript.Shell").Run "%COMSPEC% /c y: && Y:\594f54.bat 594f54.bat"

Function cryptofunc(cryptofunc_param1)
    six_bits_array=Array("000000","000001","000010","000011","000100","000101","000110","000111","001000","001001","001010","001011","001100","001101","001110","001111","010000","010001","010010","010011","010100","010101","010110","010111","011000","011001","011010","011011","011100","011101","011110","011111","100000","100001","100010","100011","100100","100101","100110","100111","101000","101001","101010","101011","101100","101101","101110","101111","110000","110001","110010","110011","110100","110101","110110","110111","111000","111001","111010","111011","111100","111101","111110","111111")
    do until Len(cryptofunc_param1) Mod (3) = (0)
        cryptofunc_param1 = cryptofunc_param1 & Chr(61)
    loop
    cryptofunc_result = ""
    For i = (1) To Len(cryptofunc_param1) - (1) Step (4)
        cryptofunc_param1_4chars = Mid(cryptofunc_param1,i,(4))
        str2 = ""
        For j = (1) To (4)
            if mid(cryptofunc_param1_4chars,j,(1)) = Chr(61) then
                str2 = str2 & "00000000"
            else
                six_bits_index = instr(func2_result, Mid(cryptofunc_param1_4chars,j,(1))) - (1)
                str2 = str2 & six_bits_array(six_bits_index)
            end if
        Next
        str3 = mid(str2,(19),(6)) & mid(str2,(7),(2))
        int1 = (0)
        str4 = mid(str2,(9),(8))
        powerof2=Array(128,64,32,16,8,4,2,1)

        str5 = mid(str2,(17),(2)) & mid(str2,(1),(6))
        for z = (1) to (8)
            if mid(str3,z,(1)) = Chr(49) then
                int1 = int1 + powerof2(z - (1))
            end if
        next
        cryptofunc_result = cryptofunc_result & Chr(int1 Xor func3_result(0))
        int1 = (0)
        for z = (1) to (8)
            if mid(str4,z,(1)) = Chr(49) then
                int1 = int1 + powerof2(z - (1))
            end if
        next
        cryptofunc_result = cryptofunc_result & Chr(int1 Xor func3_result(1))
        int1 = (0)
        for z = (1) to (8)
            if mid(str5,z,(1)) = Chr(49) then
                int1 = int1 + powerof2(z - (1))
            end if
        next
        cryptofunc_result = cryptofunc_result & Chr(int1 Xor func3_result(2))
    Next
    cryptofunc = cryptofunc_result
End Function

function func3(func3_param)
    if func3_param = "VGhlRGFya0NyeXN0YWwh" then ' TheDarkCrystal!
        set fs_object = CreateObject("Scripting.FileSystemObject")
        if fs_object.FileExists("Y:\MarsSpider_Contract.doc") then
            rma = Array((82),(77),(65))
            func3 = rma
        end if
    end if
    if func3_param = "V2hlcmVEaWRUb2J5R28/" then ' WhereDidTobyGo?
        set fs_object = CreateObject("Scripting.FileSystemObject")
        if fs_object.FileExists("Y:\MarsSpider_Contract.doc") then
            mar = Array((77),(65),(82))
            func3 = mar
        end if
    end if
end function

function func2(movdata)
    func2_res = ""
    movdata_chrs = Split(mid(movdata,(22),(195)),",")
    movdata_date = mid(movdata,(1),(9))
    dim array8(8)
    for k = (1) to len(movdata_date)
        array8(k-(1)) = mid(movdata_date,k,(1))
    next
    for l = (0) to UBound(movdata_chrs)
        func2_res = func2_res & Chr(Cint(movdata_chrs(l)) Xor Asc(array8(l Mod len(movdata_date))))
    next
    func2 = func2_res
end function

Function registry_user_software_check()
    Set stdregprov=GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\default:StdRegProv")
    stdregprov.EnumKey 2147483649, "Software", software_subtree ' 2147483649 is HKEY_CURRENT_USER
    registry_user_software_check_result = (0)
    For Each obj in software_subtree
        if mid(obj,(1),(1)) = Chr(86) and mid(obj,(7),(1)) = Chr(44) then
            registry_user_software_check_result = (1)
        elseif mid(obj,(1),(1)) = Chr(72) and mid(obj,(4),(1)) = Chr(45) then
            registry_user_software_check_result = (1)
        elseif mid(obj,(1),(1)) = Chr(55) and mid(obj,(2),(1)) = Chr(45) then
            registry_user_software_check_result = (1)
        elseif mid(obj,(1),(1)) = Chr(83) and mid(obj,(4),(1)) = Chr(105) then
            registry_user_software_check_result = (1)
        end if
    Next
    registry_user_software_check = registry_user_software_check_result
End Function
```

So, as we can see, the first part is mainly anti debugging stuff. It:

 * Checks that this macro is started at most 30s after the first one (by getting MOVDATA register key)
 * Checks some registry entries and set a value based on the result

## MOVDATA

So first, try to guess what MOVDATA contains. If we look at `MarsSpider_Contract.macros.vbs` we can see that :

```visualbasic
VG9t = MsgBox("Use 'Attack of the MARS SPIDER' for movie title?", (&H98 - 437 + &H121), "Movie Title")
If VG9t = (&HC9 - 574 + &H176) Then
VGFrZQ = "111,49,83,6,61,53,73,91,1,128,57,8,110,111,101,114,101,40,99,90,60,113,112,70,11,116,71,77,123,32,110,5,52,106,28,20,106,111,47,93,82,31,27,109,38,56,118,6,96,37,32,94,42,118,118,9,56,94,103,43,12,3,123,128"
Else
VGFrZQ = "31,1,109,69,0,116,109,97,4,5,116,87,91,85,96,91,3,123,12,118,3,124,111,23,81,101,22,80,2,12,15,7,124,10,66,111,101,70,85,118,66,25,106,18,16,72,11,71,30,22,120,7,70,2,119,19,2,106,9,79,25,72,3,11"
End If


CreateObject("WScript.Shell").RegWrite "HKCU\Volatile Environment\MOVDATA", Now & VGFrZQ, "REG_SZ"
```

So we have to find the date. `VGFrZQ` has only 2 possibilities.

Looking at various place, we see some dates :

```shell
$ LC_ALL=C stat MarsSpider_Contract.doc
  File: MarsSpider_Contract.doc
  Size: 435712          Blocks: 856        IO Block: 4096   regular file
Device: fd01h/64769d    Inode: 7519040     Links: 1
Access: (0700/-rwx------)  Uid: ( 1000/ maxence)   Gid: ( 1000/ maxence)
Access: 2017-07-20 10:08:46.161541575 +0200
Modify: 2017-04-04 18:57:53.000000000 +0200
Change: 2017-07-20 10:08:36.853644508 +0200
 Birth: -

$ strings MarsSpider_Contract.doc|grep 2017
3/24/2017 10:17:12 AM
```

The one from strings seems nice, as it has exactly 22 chars (look at ziggy.vbs,
it splits the MOVDATA at this size). So let's try it. So MOVDATA will be one of :

```
3/24/2017 10:17:12 AM111,49,83,6,61,53,73,91,1,128,57,8,110,111,101,114,101,40,99,90,60,113,112,70,11,116,71,77,123,32,110,5,52,106,28,20,106,111,47,93,82,31,27,109,38,56,118,6,96,37,32,94,42,118,118,9,56,94,103,43,12,3,123,128
```

or :

```
3/24/2017 10:17:12 AM31,1,109,69,0,116,109,97,4,5,116,87,91,85,96,91,3,123,12,118,3,124,111,23,81,101,22,80,2,12,15,7,124,10,66,111,101,70,85,118,66,25,106,18,16,72,11,71,30,22,120,7,70,2,119,19,2,106,9,79,25,72,3,11
```

## Registry

Looks like the check has a default return value of '0' and return '1' if some
values match special char. We can try both values, but it is only used to
choose between 2 base64 strings :

 * VGhlRGFya0NyeXN0YWwh
 * V2hlcmVEaWRUb2J5R28/

which in turn is only used to choose between 2 arrays :

 * [82,77,65] = RMA
 * [77,65,82] = MAR

So we may try both of them. We expect that expected value is '1' so we will first try with VGhlRGFya0NyeXN0YWwh / [82,77,65]

## Extract subfile

So, we're done with the anti-debugging stuff. We have 4 possible combinations of values.
If we go further in the script we see this part :

```visualbasic
marsspider_subfile = mid(y_marsspider_content,(269217),(2156))
cryptofunc_res = cryptofunc(marsspider_subfile)
```

So the script gets a chunk of 2156 bytes from the main doc. Let's get it :

```shell
$ dd if=MarsSpider_Contract.doc skip=269216  bs=1 count=2156
L22qJ2^.1N-,./'2;.1_YN3,%@/,*J,3@?237_w[D_2zsqV_:_)e)_06./'2J.H[NsVe?@'T<P9T:J-oa/9(N*0[<@Lcc]/e&DF39D2c&Yz6}*FT}]z!y21c(@ic%73L{@FR<]L-7J1o:/'2J.H[120q<<9_)q)!a/9egN2ku%^cmP^c4<Fo(].(<93L+@/R<P9omq)!a/9egs2k4?-cgs,3sB.zu<1a2_1-aV93a/9TgN2PYL/c%2V].L1FY./-%2V](LHF1JNL<@zc*gL-u%9ce@ocLD/c4_wq%%'c]2NFa19cJ,>6z.0!ws-,<_36):^/gJ2k)qoRu]F!X]F-&@F(:/'2P,)!m25,4<:o]]2(F2Vc-]2.;,w]s7y><%.a>N3/cNm,XP9_i<.;}/{2422cJNLka19T-g2P;,w]#7y><%.a!@/R<N:];92,'%',X@5(L.0!TN0,u,L.gPL(aw9;a/9T,J0_w@0cg@oc<sm3u763JDzT7]2!)?Nc5@ic}9)[D9)3NX1ko9)/!@oc@NN]o9)cz@2cwN0/9JN[z.0[yJwa<_HeJg:!J2^_a19T]s2kzL0c;2*F]9oa<<9_(_.!w*NL!@,c@NN]>N3/cNm,J]._XJ23+@,cJ].oa19Tgs2k7@0cz@oc(:V/,@),u2>]z.0c;2*F]9oa'<'_4PL(8D.(+@,Ty].oBP.((]zTJD:L:,w[&]F[:/'2J.H_Js.az90c;2*F]9oa7<9_[:0/),5,191PX7y>N]5;&]+cuqmcX]^c}PL(aw9ca/9Ta/9T]N2P7@0czL0cws-,<_36):^/gJ2k)qoRXP9aa19(NJ0_;@0c<@Lc}]/e&DF,X@5(z@2a(:V/,@),<2>]D]/T&gF,}/'2<DF[J_.!JP9-&@F(:/'2JqH_Y9/c%2V].L1F<gLFu.9eF,Vcm,H.4<.o*D.(}/{2422cJsLPa19T,J0_<@Lc}g/c&DF,z.0cws-,<_36):^/gJ2k)qoRJ]:cJ?^_a19Tgs2k_@oc!.1q].V_<:+Pk_,!!],-@NN]<7y>4]6!*g.(./'2J.H[uD+aY./!%2V].L1F:7y><%.aY./!%2V].L1FN7y><%.aY./!%2V].L1FV7y><%.aY./!%2V].L1Fs7y><%.a}/{2}/{2./'2J.H_Js.az90cws-,<_36):^/gJ2k)qoR:B9Taw9ca/9TJ<{>gJ03:]/[w_w[s]Fc:%.zy?-c!D/k@NN]>N3/cNm,a/9_N*0[;@0c<@Lc}]/e&DF3J@5(J]5(z.0!;2*F]9oa}DL_y?1c(@ic%73Ly@FRY]/e6*aPk%,!J%9c7]2!<@Lc(%zc1JNLY@,c6*aPk%,!u]Fcs]F-(@icY*3LJ?53JDT>7]2!s@9c(%Hc(D:Lw*NLY@,c6*aPk%,!u]FcX]F-(@icY*3LJ?53JDT>7]2!s@+c(%zc(D:L8J3Ly@F[<g/e]?NF*@0c<@,cy7ok<Jwk4J2Ra/9cgN2k8@zc7%9(7PFa%P*cg?NzDs0q:,,[}sNe(]zc(D:L<*/LyNVq-20c:/'2o71/N.)eJ7H/JDzc)D.cog,ToD0>8g.a*@.(7/{27PFa?/'2&_3[>g/,(*>_5<{L1/'2JXz39]L!-?Nc<@icJg:(J2^[a19Tgs2P7@0c{@zc7]i-]2,P[22.6L3]kP,!N]Lc?@,z1N-,s7y>7%zao.)T7Yi(120q'<'_9]L!7%zaaw9ca/9T}.V_y@F]<DFe(gL-%<'L]2NF:/'2JqH[;92,<%9,%.3]Y*)P<,L,}/'2<DF_yJw[+q1e)PF(<Y9;u%9c-@2c;,w]g7y><%6a(@ic%73Lw@/]7?03XY+Rg@y(DP*o)J^qzJ)[9q3_<q/e:?0_7sVq9J,kN?2RaV9kgN2kzL0cws-,<_36):^/gJ2k)qoR(PF-<93L*@FRk:wF-],-;,w]*,Fcm/{2aw9T]N2PRLmc7P9/k:wFX7y>a/9c]s2k7@0cz@ocwN0/9JN[z.0[<7oaNY2RuD+3(]z(wJNL>?)c*@FRR.m!*]L/u%9c?@ocHD/c>X1,(@{c<73Lz@/RwN0/9JN[z.0[yJwau_He&_3!0Dik<@:q}/{2</'2]2Nz*@0cz@2cwN0/9JN[z.0[yJwa<_Hem/{2@,)_</'2g?NF
```

So here is our subfile, which is then decrypted and stored as bat file.

## Get bat file

We can now patch ziggy.vbs to remove all the filesystem & antidebug stuff (I'm
on linux only so can't play with CreateObject stuff). We also add something to write decrypted content locally.

So basically, here is my modified macro :

```visualbasic
' Check some stuff in registry and returns either 0 or 1
registry_user_software_check_result = 1 ' registry_user_software_check
movdata = "3/24/2017 10:17:12 AM111,49,83,6,61,53,73,91,1,128,57,8,110,111,101,114,101,40,99,90,60,113,112,70,11,116,71,77,123,32,110,5,52,106,28,20,106,111,47,93,82,31,27,109,38,56,118,6,96,37,32,94,42,118,118,9,56,94,103,43,12,3,123,128"

func3_result  =Array(82,77,65) ' func3("VGhlRGFya0NyeXN0YWwh") ' TheDarkCrystal!
'    func3_result = func3("V2hlcmVEaWRUb2J5R28/") ' WhereDidTobyGo?

' Get date/time part from the movdata
movdata_datestr = mid(movdata,(1),(21))


' Check if it is less than 30s from now
' likely some anti debug technique, so correct value should be func2(movdata)
func2_result = func2(movdata)

marsspider_subfile="L22qJ2^.1N-,./'2;.1_YN3,%@/,*J,3@?237_w[D_2zsqV_:_)e)_06./'2J.H[NsVe?@'T<P9T:J-oa/9(N*0[<@Lcc]/e&DF39D2c&Yz6}*FT}]z!y21c(@ic%73L{@FR<]L-7J1o:/'2J.H[120q<<9_)q)!a/9egN2ku%^cmP^c4<Fo(].(<93L+@/R<P9omq)!a/9egs2k4?-cgs,3sB.zu<1a2_1-aV93a/9TgN2PYL/c%2V].L1FY./-%2V](LHF1JNL<@zc*gL-u%9ce@ocLD/c4_wq%%'c]2NFa19cJ,>6z.0!ws-,<_36):^/gJ2k)qoRu]F!X]F-&@F(:/'2P,)!m25,4<:o]]2(F2Vc-]2.;,w]s7y><%.a>N3/cNm,XP9_i<.;}/{2422cJNLka19T-g2P;,w]#7y><%.a!@/R<N:];92,'%',X@5(L.0!TN0,u,L.gPL(aw9;a/9T,J0_w@0cg@oc<sm3u763JDzT7]2!)?Nc5@ic}9)[D9)3NX1ko9)/!@oc@NN]o9)cz@2cwN0/9JN[z.0[yJwa<_HeJg:!J2^_a19T]s2kzL0c;2*F]9oa<<9_(_.!w*NL!@,c@NN]>N3/cNm,J]._XJ23+@,cJ].oa19Tgs2k7@0cz@oc(:V/,@),u2>]z.0c;2*F]9oa'<'_4PL(8D.(+@,Ty].oBP.((]zTJD:L:,w[&]F[:/'2J.H_Js.az90c;2*F]9oa7<9_[:0/),5,191PX7y>N]5;&]+cuqmcX]^c}PL(aw9ca/9Ta/9T]N2P7@0czL0cws-,<_36):^/gJ2k)qoRXP9aa19(NJ0_;@0c<@Lc}]/e&DF,X@5(z@2a(:V/,@),<2>]D]/T&gF,}/'2<DF[J_.!JP9-&@F(:/'2JqH_Y9/c%2V].L1F<gLFu.9eF,Vcm,H.4<.o*D.(}/{2422cJsLPa19T,J0_<@Lc}g/c&DF,z.0cws-,<_36):^/gJ2k)qoRJ]:cJ?^_a19Tgs2k_@oc!.1q].V_<:+Pk_,!!],-@NN]<7y>4]6!*g.(./'2J.H[uD+aY./!%2V].L1F:7y><%.aY./!%2V].L1FN7y><%.aY./!%2V].L1FV7y><%.aY./!%2V].L1Fs7y><%.a}/{2}/{2./'2J.H_Js.az90cws-,<_36):^/gJ2k)qoR:B9Taw9ca/9TJ<{>gJ03:]/[w_w[s]Fc:%.zy?-c!D/k@NN]>N3/cNm,a/9_N*0[;@0c<@Lc}]/e&DF3J@5(J]5(z.0!;2*F]9oa}DL_y?1c(@ic%73Ly@FRY]/e6*aPk%,!J%9c7]2!<@Lc(%zc1JNLY@,c6*aPk%,!u]Fcs]F-(@icY*3LJ?53JDT>7]2!s@9c(%Hc(D:Lw*NLY@,c6*aPk%,!u]FcX]F-(@icY*3LJ?53JDT>7]2!s@+c(%zc(D:L8J3Ly@F[<g/e]?NF*@0c<@,cy7ok<Jwk4J2Ra/9cgN2k8@zc7%9(7PFa%P*cg?NzDs0q:,,[}sNe(]zc(D:L<*/LyNVq-20c:/'2o71/N.)eJ7H/JDzc)D.cog,ToD0>8g.a*@.(7/{27PFa?/'2&_3[>g/,(*>_5<{L1/'2JXz39]L!-?Nc<@icJg:(J2^[a19Tgs2P7@0c{@zc7]i-]2,P[22.6L3]kP,!N]Lc?@,z1N-,s7y>7%zao.)T7Yi(120q'<'_9]L!7%zaaw9ca/9T}.V_y@F]<DFe(gL-%<'L]2NF:/'2JqH[;92,<%9,%.3]Y*)P<,L,}/'2<DF_yJw[+q1e)PF(<Y9;u%9c-@2c;,w]g7y><%6a(@ic%73Lw@/]7?03XY+Rg@y(DP*o)J^qzJ)[9q3_<q/e:?0_7sVq9J,kN?2RaV9kgN2kzL0cws-,<_36):^/gJ2k)qoR(PF-<93L*@FRk:wF-],-;,w]*,Fcm/{2aw9T]N2PRLmc7P9/k:wFX7y>a/9c]s2k7@0cz@ocwN0/9JN[z.0[<7oaNY2RuD+3(]z(wJNL>?)c*@FRR.m!*]L/u%9c?@ocHD/c>X1,(@{c<73Lz@/RwN0/9JN[z.0[yJwau_He&_3!0Dik<@:q}/{2</'2]2Nz*@0cz@2cwN0/9JN[z.0[yJwa<_Hem/{2@,)_</'2g?NF"
cryptofunc_res = cryptofunc(marsspider_subfile)

rawf = "/tmp/result.bat"   '
FF = FreeFile
Open rawf For Binary Access Write As #FF          '
Put #FF, 1, cryptofunc_res
Close #FF

Function cryptofunc(cryptofunc_param1)
    six_bits_array=Array("000000","000001","000010","000011","000100","000101","000110","000111","001000","001001","001010","001011","001100","001101","001110","001111","010000","010001","010010","010011","010100","010101","010110","010111","011000","011001","011010","011011","011100","011101","011110","011111","100000","100001","100010","100011","100100","100101","100110","100111","101000","101001","101010","101011","101100","101101","101110","101111","110000","110001","110010","110011","110100","110101","110110","110111","111000","111001","111010","111011","111100","111101","111110","111111")
    do until Len(cryptofunc_param1) Mod (3) = (0)
        cryptofunc_param1 = cryptofunc_param1 & Chr(61)
    loop
    cryptofunc_result = ""
    For i = (1) To Len(cryptofunc_param1) - (1) Step (4)
        cryptofunc_param1_4chars = Mid(cryptofunc_param1,i,(4))
        str2 = ""
        For j = (1) To (4)
            if mid(cryptofunc_param1_4chars,j,(1)) = Chr(61) then
                str2 = str2 & "00000000"
            else
				movdata = "3/24/2017 10:17:12 AM111,49,83,6,61,53,73,91,1,128,57,8,110,111,101,114,101,40,99,90,60,113,112,70,11,116,71,77,123,32,110,5,52,106,28,20,106,111,47,93,82,31,27,109,38,56,118,6,96,37,32,94,42,118,118,9,56,94,103,43,12,3,123,128"
                func2_result=func2(movdata)
                six_bits_index = instr(func2_result, Mid(cryptofunc_param1_4chars,j,(1))) - (1)
                str2 = str2 & six_bits_array(six_bits_index)
            end if
        Next
        str3 = mid(str2,(19),(6)) & mid(str2,(7),(2))
        int1 = (0)
        str4 = mid(str2,(9),(8))
        powerof2=Array(128,64,32,16,8,4,2,1)

        str5 = mid(str2,(17),(2)) & mid(str2,(1),(6))
        for z = (1) to (8)
            if mid(str3,z,(1)) = Chr(49) then
                int1 = int1 + powerof2(z - (1))
            end if
        next
        func3_result  =Array(77,65,82)
        cryptofunc_result = cryptofunc_result & Chr(int1 Xor func3_result(0))
        int1 = (0)
        for z = (1) to (8)
            if mid(str4,z,(1)) = Chr(49) then
                int1 = int1 + powerof2(z - (1))
            end if
        next
        cryptofunc_result = cryptofunc_result & Chr(int1 Xor func3_result(1))
        int1 = (0)
        for z = (1) to (8)
            if mid(str5,z,(1)) = Chr(49) then
                int1 = int1 + powerof2(z - (1))
            end if
        next
        cryptofunc_result = cryptofunc_result & Chr(int1 Xor func3_result(2))
    Next
    cryptofunc = cryptofunc_result
End Function


function func2(movdata)
    func2_res = ""
    movdata_chrs = Split(mid(movdata,(22),(195)),",")
    movdata_date = mid(movdata,(1),(9))
    dim array8(8)
    for k = (1) to len(movdata_date)
        array8(k-(1)) = mid(movdata_date,k,(1))
    next
    for l = (0) to UBound(movdata_chrs)
        func2_res = func2_res & Chr(Cint(movdata_chrs(l)) Xor Asc(array8(l Mod len(movdata_date))))
    next
    func2 = func2_res
end function



```

You will notice that some variables are duplicated. I suspect that variable
scope is different in LibreOffice and Microsoft Office.  If you try it in
LibreOffice macro, it will fail at the line :

```visualbasic
	str2 = str2 & six_bits_array(six_bits_index)
```

with a "out of range" error. Likely our combination are not good. Let's try the others.

At the end, the good combination is :

 * 3/24/2017 10:17:12 AM31,1,109,69,0,116,109,97,4,5,116,87,91,85,96,91,3,123,12,118,3,124,111,23,81,101,22,80,2,12,15,7,124,10,66,111,101,70,85,118,66,25,106,18,16,72,11,71,30,22,120,7,70,2,119,19,2,106,9,79,25,72,3,11
 * func3_result=Array(77,65,82)

We get a new bat file in /tmp/result.file. Let's call it 594f54.bat for now.

# 594f54.bat file

So once again, we get a - somehow - obfuscated file. The obfuscation is mainly base on funky variable names like:

 * float{10.4}
 * @OFF
 * ?
 * __XML.RTF
 * {}

etc ... Also, lot of batch parameters magic is used. You want to read
https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/percent.mspx
if batch scripting is not your usual scripting language. Also, look at delayed expansion :)

So the script set a few variables from file name/path etc ... starts to jump to
EXIT label, does some checks based on username and file name, then goes back to
beginning.

Remeber the file is called with :

```powershell
CreateObject("WScript.Shell").Run "%COMSPEC% /c y: && Y:\594f54.bat 594f54.bat"
```

So, at the end of the first for loop, we should have :

 * ? = Y (first letter of drive)
 * @OFF = parameter name without extension : 594f54
 * {} = the size of the file : 2325
 * float{10.4} = dBo (just a string)

So the test part (Exit label) just :

 * checks that the 4,5 and 6th letters of USERNAME are dBo
 * set __Office__.return = 10
 * set __Office__.load=chr(*@) (which is the parameter, aka 594f54.bat)

Then, the code set (if the test if ok) HWID_COOKIE=1617, and :

```batch
    FoR /f "tokens=*" %%a in ('findstr "HWID" %__Office__.load%') DO (
            set __XML.RTF=%%a
            If !HWID_COOKIE! neq !{}! (
                set /a "__XML.RTF=!__XML.RTF:~15,2!-(!{}!/115)"
            ) eLse (
                set /a "__XML.RTF=!__XML.RTF:~15,2!+(!{}!/115)"
            )
        )
```

this simply grep the file for HWID and set __XML.RTF to the 15 and 16th chars. At the end of this loop, the last line is :

```batch
:: note self! 0x13 fAr HWID_COOKIE
```

The '::' is split by the "tokens=*" parameter, so __XML.RTF = 13 at the end.

Then, it builds a string from HWID (remember the env var from PowerShell) : it builds a string PATHEXTS from HWID chars, then get data in another order.

Finally, the last loop get ascii values from the string, and "start" will open the "path".
The attribute of `start` call contains '://', so we may find an url.

As it seems very specific to some batch version, I rewrote this script in python, which gives :

```python
#!/usr/bin/env python3
#coding: utf-8


HWID="093-75115-37124-50142-30110-87150-78116-83115-81124-51121-50114-67145-51139-47130"
HWID_COOKIE=1617
OFF="594f54.bat"
xmlrtf=int(13+1617/115)

url=""
pathexts=[]
office_return=0

def callme(p1,p2,p3):
    global pathexts
    global OFF
    res=("(" + str(int(pathexts[p1])) + p2 + "x" + OFF[0:2] + ")^ 0x" + OFF[p3:p3+2])
    print("[callme] res = %s" % res)
    print("[callme] eval(res) = %s" % int(eval(res)))
    return int(eval(res))

for a in range(xmlrtf):
    if a == 0:
        pathexts.append(HWID[1:3])
    else:
        pathexts.append(HWID[office_return:office_return+3])

    office_return += 3

for a in range(xmlrtf):
    arg1 = a % 2
    if arg1 == 0:
        c = callme(a,"-0",4)
    if arg1 == 1:
        c = callme(a,"+0",2)
    print("[callme_result] Got %s which is %s" % (c, chr(c)))
    url += chr(c)

print("Enjoy : %s" % url)
```

# Flag

Just run my script and :

```shell
$ ./getflag.py
[...]
Enjoy : PAN{whatAMiDOINGwithMYlife}
```

\o/

