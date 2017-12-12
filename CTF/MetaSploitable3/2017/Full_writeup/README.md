# MetaSploitable3 Community CTF

### 5 of hearts

Once the platform had started we did the usual things.  
The nmap scan showed an open port 80 so let's have a look there.

A quick ssh tunnel later and we have a directory listing, and a drupal folder.

On the drupal site we find and article called `I <3 High-Fives!` that contains a picture:  


![alt text](5_of_hearts.png "")

Good start...

But the challenge mentions donuts and I can't see any here, seems like a classic steganography challenge to me.  
Zsteg to the rescue!

In the text fields we get a HYUGE base64 blob, which unsurprisingly turns in to a PNG when decoded.  


![alt text](5_hearts2.png "DONUTS!")

Ahh donuts, and a flag.

### 8 of hearts

While I was working of the 5 of hearts, my collegue who is a whiz at SQLI had gotten the database root password from the payroll_app.php  
So we had a look at the database and found the "super_secret_db", looks interesting.

One table called flags containing a blob...  
We downloaded it and ran binwalk. This yielded a zip file, an encrypted zip file.  
But we don't have a password.

Seeing as time was an issue I thought I'd run fcrackzip on it just in case while I looked around to see if it was hidden in the database.  
Turns out I didn't even get a chance to look, fcrackzip and the rockyou password list got it in just over a second:


![alt text](8_of_hearts.png "")


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
