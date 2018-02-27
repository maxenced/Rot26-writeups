Zip Attack
==========

In this challenge we got an [encrypted](encrypted.zip) file. We also got [another zip](unencrypted.zip), with one of the file which is also in encrypted zip:

```bash
$ zipinfo encrypted.zip
Archive:  encrypted.zip
Zip file size: 186312 bytes, number of entries: 3
drwxr-xr-x  3.0 unx        0 bx stor 18-Feb-23 02:53 supersecretstuff/
-rw-r--r--  3.0 unx       34 TX stor 18-Feb-23 02:53 supersecretstuff/flag.txt
-rw-r--r--  3.0 unx   220680 BX defX 18-Feb-23 02:48 supersecretstuff/sw-iphone-wallpaper-first-order.jpg
3 files, 220714 bytes uncompressed, 185662 bytes compressed:  15.9%
```

```bash
$ zipinfo known-file.zip
Archive:  known-file.zip
Zip file size: 185848 bytes, number of entries: 1
-rw-r--r--  3.0 unx   220680 bx defX 18-Feb-23 02:40 sw-iphone-wallpaper-first-order.jpg
1 file, 220680 bytes uncompressed, 185628 bytes compressed:  15.9%
```

You can get some details about plaintext attack on zip [here](http://www.delaat.net/rp/2014-2015/p57/report.pdf).

Pkcrack tool is able to recover password with plaintext, so just do it :

```bash
$ pkcrack -C encrypted.zip -P known-file.zip  -c supersecretstuff/sw-iphone-wallpaper-first-order.jpg -p sw-iphone-wallpaper-first-order.jpg -a -d decrypted.zip
Files read. Starting stage 1 on Tue Feb 27 15:33:18 2018
Generating 1st generation of possible key2_185639 values...done.
Found 4194304 possible key2-values.
Now we're trying to reduce these...
Lowest number: 988 values at offset 181903
Lowest number: 962 values at offset 181892
Lowest number: 922 values at offset 181862
Lowest number: 915 values at offset 181861
Lowest number: 904 values at offset 181858
Lowest number: 890 values at offset 178046
Lowest number: 845 values at offset 178043
Lowest number: 813 values at offset 178006
Lowest number: 807 values at offset 178000
Lowest number: 803 values at offset 177993
Lowest number: 782 values at offset 177987
Lowest number: 766 values at offset 177984
Lowest number: 709 values at offset 177978
Lowest number: 668 values at offset 177975
Lowest number: 649 values at offset 177817
Lowest number: 626 values at offset 177816
Lowest number: 604 values at offset 177791
Lowest number: 580 values at offset 177790
Lowest number: 531 values at offset 177781
Lowest number: 528 values at offset 177714
Lowest number: 471 values at offset 177712
Lowest number: 414 values at offset 177672
Lowest number: 399 values at offset 177670
Lowest number: 389 values at offset 177668
Lowest number: 378 values at offset 177667
Lowest number: 338 values at offset 177662
Lowest number: 321 values at offset 177654
Lowest number: 287 values at offset 177631
Lowest number: 274 values at offset 177629
Lowest number: 251 values at offset 177623
Lowest number: 243 values at offset 177620
Lowest number: 241 values at offset 155670
Lowest number: 233 values at offset 155669
Lowest number: 226 values at offset 155657
Lowest number: 206 values at offset 155655
Lowest number: 202 values at offset 155653
Lowest number: 190 values at offset 155651
Lowest number: 154 values at offset 155650
Lowest number: 148 values at offset 155646
Lowest number: 137 values at offset 155645
Lowest number: 127 values at offset 155630
Lowest number: 123 values at offset 149511
Lowest number: 121 values at offset 149509
Lowest number: 112 values at offset 149474
Lowest number: 109 values at offset 149468
Lowest number: 103 values at offset 149458
Lowest number: 100 values at offset 149456
Done. Left with 100 possible Values. bestOffset is 149456.
Stage 1 completed. Starting stage 2 on Tue Feb 27 15:33:37 2018
Ta-daaaaa! key0=b411ca07, key1=88d0ea9c, key2=1fe5493a
Probabilistic test succeeded for 36188 bytes.
Ta-daaaaa! key0=b411ca07, key1=88d0ea9c, key2=1fe5493a
Probabilistic test succeeded for 36188 bytes.
Ta-daaaaa! key0=b411ca07, key1=88d0ea9c, key2=1fe5493a
Probabilistic test succeeded for 36188 bytes.
Ta-daaaaa! key0=b411ca07, key1=88d0ea9c, key2=1fe5493a
Probabilistic test succeeded for 36188 bytes.
Ta-daaaaa! key0=b411ca07, key1=88d0ea9c, key2=1fe5493a
Probabilistic test succeeded for 36188 bytes.
Ta-daaaaa! key0=b411ca07, key1=88d0ea9c, key2=1fe5493a
Probabilistic test succeeded for 36188 bytes.
Stage 2 completed. Starting zipdecrypt on Tue Feb 27 15:33:38 2018
Decrypting supersecretstuff/flag.txt (0c9af138e6ef46b0236ba996)... OK!
Decrypting supersecretstuff/sw-iphone-wallpaper-first-order.jpg (b4b787fdee624b8ea2ab0a96)... OK!
Finished on Tue Feb 27 15:33:38 2018
```

And get the flag :

```bash
$ unzip decrypted.zip
Archive:  decrypted.zip
replace supersecretstuff/flag.txt? [y]es, [n]o, [A]ll, [N]one, [r]ename: A
 extracting: supersecretstuff/flag.txt
 inflating: supersecretstuff/sw-iphone-wallpaper-first-order.jpg

$ cat supersecretstuff/flag.txt
flag{plaintext-attacks-are-cool!}
```

