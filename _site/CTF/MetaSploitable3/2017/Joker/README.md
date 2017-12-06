# MetaSploitable3 Community CTF

### Joker

After rooting the machine we had free range of the file system.  
A quick find command showed us all the png files available, including:
`/etc/joker.png`

Aha, easy flag right? well no, the MD5 hash didn't work..  
Looking at the picture we see it's a negative, so we'll just use convert:  
`$convert joker.png -negate joker2.png`

Nop, still not the right flag.

Inverting the image also changes the metadata so we'll be getting the wrong hash.  
(I even tried submiting the hashes backwards in case it was a trick)

In the end I used gimp, opened the file.  
Colors > Invert gives us the right picture.  
Then File > Export as..  
Save as joker2.png  
And here's the trick, untick all the options:  
![alt text](gimp.png "")

The MD5 hash of this file was the flag.  
Turns out I was the first to find it, happy about that.
