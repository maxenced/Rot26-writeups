# Gogogobaby

Sur ce chall on récupère un fichier source go. La partie intéressante est la fonction _saxxCustomAlgorithmOrNot_.

On voit également que le résultat à déchiffrer est _4a1b506c33694e055f9605555550a4a5a54ad2d7227266226322e4afd2a0f0227de4224ebb9cb1a5d22250a5221ee49939224e22501e05227d22721111721e50a4a5a50455555088_.

En étudiant la fonction on se rend compte que ça fait:

 * un bitshift vers la gauche 2 bits
 * un xor entre la valeur initiale et le bitshift
 * un xor entre une variable "init" et la valeur obtenue par l'opération précédente

Au final, chaque caractère est la valeur de la variable "init" à la fin de l'itération (avec un masque à 0xff).
Avant l'itération suivante, init est décalée de 8 bits vers la droite.
La valeur "init" évolue donc à chaque itération.

Au final, on a la chaine à obtenir et l'algo. Il y aurait plus élégant mais ça se bruteforce facile, on a au plus 18360 combinaisons à tester (255 * la taille de la chaine )

On bruteforce avec quelques lignes de Python:

```python
#!/usr/bin/env python
s="4a1b506c33694e055f9605555550a4a5a54ad2d7227266226322e4afd2a0f0227de4224ebb9cb1a5d22250a5221ee49939224e22501e05227d22721111721e50a4a5a
50455555088".decode('hex')
init = 0
res = ""
for c in s:
    for i in range(0,255):
        old_init = init
        init = init ^ ((i << 2) ^ i)
        to_test = init & 0xff
        if to_test == ord(c):
            res += chr(i)
            init = init >> 8

        else:
            init = old_init

print "Flag is %s" % res
```

Et on obtient:

```
python breakgo.py
Flag is BREIZHCTF{TDDE!tttBon_OK_J_avoue_La_Crypto_Et_SaxX_C_EST_L_OPPOSE!tttTDDE}
```
