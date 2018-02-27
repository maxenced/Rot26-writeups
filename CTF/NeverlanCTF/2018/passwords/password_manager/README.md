The Password Manager
====================

This challenge was quiet cool as I never played with 1password vault before. Still, this was again a bruteforce :(.

So, we got a 1password (opvault format) vault, and a test one with given password `test`.

Looks like one tool for playing with opvault vaults is [available on GitHub](https://github.com/OblivionCloudControl/opvault).

Let's take our favorite wordlist and test it.

Note: the following code is not optimized at all (not even parallelized) but did the job:

```python
#!/usr/bin/env python3
from opvault.onepass import OnePass
from opvault import exceptions
from opvault import designation_types
from pwn import *

log.info('Load Password file')
with open('10k_most_common.txt','r', encoding='utf-8') as f:
    logger = log.progress('Testing ')
    for p in f.readlines():
        logger.status(p.strip())
        master_password = p.strip()

        try:
            vault = OnePass('testvault.opvault')
            vault.unlock(master_password=master_password)
        except exceptions.OpvaultException:
            pass
        else:
            logger.success(p)
            vault.load_items()

            log.info(vault.getItems())
            for item in vault.getItems().keys():
                overview, details = vault.get_item(item)
                password = [field['value'] for field in details['fields']
                            if field['designation'] == designation_types.DesignationTypes.PASSWORD][0]

                log.info("%s : %s" % (item,password))
            exit()
```

So we first tested with the given test vault, and got :

```
$ ./break.py
[*] Load Password file
[+] Testing : test
[*] {'google': '44E01EB2B88D40989B11B2BD7D19EB19'}
[*] google : yougotmypass
```

in a matter of seconds. Let's try the other vault with the same small wordlist before using rockyou :

```
$ ./break.py
[*] Load Password file
[+] Testing : starwars
[*] {'flag': '93B5051CDEAE418F9D2C2F224B33EF1F'}
[*] flag : flag{Wow_You_CRACKED-the-VAULT}
```

