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
