## Diffie Failman

Ici on récupère une capture ainsi qu'un bout de python qui a servir à la communication.

On voit quelques parties intéressantes :

```python
shared = 65535
private_key = randint(10**24,10**32)
public_key = shared * private_key
```

Donc client et serveur génèrent leurs clés de cette façon. Le protocole pour
décider de la clé commune est simple, chaque partie envoie sa clé publique à
l'autre partie, qui la multiplie avec sa propre clé privée. Le hash en SHA256
de cette valeur sert ensuite de shared secret.

Les fonctions de chiffrage et déchiffrage utilisent ensuite ce "shared_secret" comme clé.

## Exploit

Vu le code, on sait que le premier paquet de chaque "client" est la clé publique.
Si on a la clé publique, on connait le "shared" (= 65535), on peut donc
récupérer la clé privée de chaque partie, et donc reconstruire la clé
"intermédiaire" qui permettra de tout déchiffrer.

```bash
$ tshark -Tfields -e data.data -r  capture.pcap |tr -d ':'
34363538323837373231343738383137353031313531373235363339363938373931303430
31343439313231363732303538343338373239313339323135303030303939383530303330
[...]
```

on a donc :

    * cle pub client : 4658287721478817501151725639698791040
    * cle pub serveur: 1449121672058438729139215000099850030

on récupère donc la clé privée de chacun :

    * client : 71080914343157358680883888604544
	* serveur: 22112179324917047823898908981458

Et donc la clé intermediaire :

   	* 103004893444398851671013690478166602242546078095664609663680376536320 (priv_client * pub_serveur == priv_serveur * pub_client) 

Une fois qu'on a ça c'est quasi gagné, la suite du tshark contient les data:

```bash
$ tshark -Tfields -e data.data -r  capture.pcap |tr -d ':'
34363538323837373231343738383137353031313531373235363339363938373931303430
31343439313231363732303538343338373239313339323135303030303939383530303330
7998cfd2b12fd3be5efd845a1b638b9b3a2d7533394bc7768cbd51d4c31fc55b
01bb1c99f837f02148b46501f91ecb9d4b6f0aa6baea4a22fb81488fa23f54c2
6223e4ee738280199791e7c65a2cfcfb43648a27e9f97e61b7c3d78368c98c9539216b6da457c61d41e895df8966b270
64ff23d65f6926f1c55253e3b892a25872d44b0d48f9f0b01580958bfc1e668b5c9235e8f3ed2c0c76258152d97402604a10d507cfcbd701529dfa972afe7b4a
4f8934cac701dcb5b3a02908ad37e77ef9afd1ebe2c8dad07db1932b5fb73ced
423e44d00b30222cb8ee5e7b50e6d7511fd70c5301ad3d58cb90ce5846850374
b0ca8380fe49a450f8e64f41a4c63a8e94bd8aa8673a92952ac51be9cd6ddb1e
```

Il suffit donc de déchiffrer ça :

```python
#!/usr/bin/env python
import hashlib
from Crypto.Cipher import AES

unpad = lambda s : s[0:-ord(s[-1])]

def decrypt(message, key):
    IV = message[:AES.block_size]
    aes = AES.new(key, AES.MODE_CBC, IV)
    return unpad(aes.decrypt(message[AES.block_size:]))

intermediate = 103004893444398851671013690478166602242546078095664609663680376536320
shared_secret = hashlib.sha256(str(intermediate).encode("utf-8")).digest()

messages = [
    '7998cfd2b12fd3be5efd845a1b638b9b3a2d7533394bc7768cbd51d4c31fc55b',
    '01bb1c99f837f02148b46501f91ecb9d4b6f0aa6baea4a22fb81488fa23f54c2',
    '6223e4ee738280199791e7c65a2cfcfb43648a27e9f97e61b7c3d78368c98c9539216b6da457c61d41e895df8966b270',
    '64ff23d65f6926f1c55253e3b892a25872d44b0d48f9f0b01580958bfc1e668b5c9235e8f3ed2c0c76258152d97402604a10d507cfcbd701529dfa972afe7b4a',
    '4f8934cac701dcb5b3a02908ad37e77ef9afd1ebe2c8dad07db1932b5fb73ced',
    '423e44d00b30222cb8ee5e7b50e6d7511fd70c5301ad3d58cb90ce5846850374',
    'b0ca8380fe49a450f8e64f41a4c63a8e94bd8aa8673a92952ac51be9cd6ddb1e',
]

for message in messages:
    print(decrypt(message.decode('hex'), shared_secret))
```

Et on exécute :

```bash
$ python break.py
Hi !
Hi dude !
Can you give me the flag ?
Sure : BZHCTF{This_key_exchange_Sux}
Thx !
Bye
Bye !
```
