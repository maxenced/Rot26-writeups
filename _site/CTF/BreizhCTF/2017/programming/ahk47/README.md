# A-H-K 47

On comprend assez vite avec le fichier fourni qu'il faut remplacer la ligne :

```
#8c15e88a775a924dd0e8bb8c92d015447792b7774492fd7f29e8
```

Avec le dictionnaire en fin de fichier:

```bash
8====D::^a::#HotLikeBreizh::16
8====D::^b::#HotLikeBreizh::4d
8====D::^c::#HotLikeBreizh::8c
8====D::^d::#HotLikeBreizh::01
8====D::^e::#HotLikeBreizh::4d
8====D::^f::#HotLikeBreizh::07
8====D::^g::#HotLikeBreizh::cd
8====D::^h::#HotLikeBreizh::b7
8====D::^i::#HotLikeBreizh::bb
8====D::^j::#HotLikeBreizh::32
8====D::^k::#HotLikeBreizh::fd
8====D::^l::#HotLikeBreizh::a3
8====D::^m::#HotLikeBreizh::5a
8====D::^n::#HotLikeBreizh::30
8====D::^o::#HotLikeBreizh::71
8====D::^p::#HotLikeBreizh::4c
8====D::^q::#HotLikeBreizh::ec
8====D::^r::#HotLikeBreizh::20
8====D::^s::#HotLikeBreizh::e8
8====D::^t::#HotLikeBreizh::8a
8====D::^u::#HotLikeBreizh::15
8====D::^v::#HotLikeBreizh::bb
8====D::^w::#HotLikeBreizh::13
8====D::^x::#HotLikeBreizh::ed
8====D::^y::#HotLikeBreizh::29
8====D::^z::#HotLikeBreizh::c0
8====D::^0::#HotLikeBreizh::77
8====D::^1::#HotLikeBreizh::a7
8====D::^2::#HotLikeBreizh::a8
8====D::^3::#HotLikeBreizh::7f
8====D::^4::#HotLikeBreizh::d0
8====D::^5::#HotLikeBreizh::61
8====D::^6::#HotLikeBreizh::46
8====D::^7::#HotLikeBreizh::44
8====D::^8::#HotLikeBreizh::72
8====D::^9::#HotLikeBreizh::07
8====D::^_::#HotLikeBreizh::92
```

Ca se fait facilement avec un oneliner :

```bash
(grep 'HotLikeBreizh' enc|awk -F ':' '{ print "_"$NF"="$3 }' |tr -d '^' |xargs echo  |tr ' ' ';' ; echo -n "echo "; grep ^# enc |tr -d '#' |sed 's/\(..\)/$_\1/g')   |sh
```

Pour faire simple:

```bash
grep 'HotLikeBreizh' enc|awk -F ':' '{ print "_"$NF"="$3 }' |tr -d '^' |xargs echo  |tr ' ' ';'
```

Ca transforme chaque ligne '8====D::^_::#HotLikeBreizh::92' en '$_92=_'. Il
faut rajouter un underscore avant chaque valeur car bash n'accepte pas une
variable qui commence avec un chiffre.

Ensuite :

```bash
echo -n "echo "; grep ^# enc |tr -d '#' |sed 's/\(..\)/$_\1/g'
```

on transforme la ligne _8c15e8..._ en:

```bash
$_8c$_15$_e8
```

qui sera donc interprétée avec les variables définies sur la première étape. Ça donne donc :

```bash
$ (grep 'HotLikeBreizh' enc|awk -F ':' '{ print "_"$NF"="$3 }' |tr -d '^' |xargs echo  |tr ' ' ';' ; echo -n "echo "; grep ^# enc |tr -d '#' |sed 's/\(..\)/$_\1/g')
_16=a;_4d=b;_8c=c;_01=d;_4d=e;_07=f;_cd=g;_b7=h;_bb=i;_32=j;_fd=k;_a3=l;_5a=m;_30=n;_71=o;_4c=p;_ec=q;_20=r;_e8=s;_8a=t;_15=u;_bb=v;_13=w;_ed=x;_29=y;_c0=z;_77=0;_a7=1;_a8=2;_7f=3;_d0=4;_61=5;_46=6;_44=7;_72=8;_07=9;_92=_
echo $_8c$_15$_e8$_8a$_77$_5a$_92$_4d$_d0$_e8$_bb$_8c$_92$_d0$_15$_44$_77$_92$_b7$_77$_44$_92$_fd$_7f$_29$_e8
```

Et donc ça donne :

```bash
$ (grep 'HotLikeBreizh' enc|awk -F ':' '{ print "_"$NF"="$3 }' |tr -d '^' |xargs echo  |tr ' ' ';' ; echo -n "echo "; grep ^# enc |tr -d '#' |sed 's/\(..\)/$_\1/g')   |sh
cust0m_e4svc_4u70_h07_k3ys
```

On tente avec ce flag (entouré de bzhctf{}) sans succès. On se rend compte que e4svc veut pas dire grand chose.

En regardant de plus pret, on voit qu'il y a certains caractères qui ont la même valeur:

```bash
$ grep 'HotLikeBreizh' enc |sort -t ':' -k7
8====D::^d::#HotLikeBreizh::01
8====D::^9::#HotLikeBreizh::07
8====D::^f::#HotLikeBreizh::07
[...]
8====D::^b::#HotLikeBreizh::4d
8====D::^e::#HotLikeBreizh::4d
[...]
8====D::^i::#HotLikeBreizh::bb
8====D::^v::#HotLikeBreizh::bb
```

On tente en enlevant les 2emes chars à chaque fois (f,e et v donc) et :

```bash
(grep 'HotLikeBreizh' enc|grep -v '[fev]:' | awk -F ':' '{ print "_"$NF"="$3 }' |tr -d '^' |xargs echo  |tr ' ' ';' ; echo -n "echo "; grep ^# enc |tr -d '#' |sed 's/\(..\)/$_\1/g')   |sh
cust0m_b4sic_4u70_h07_k3ys
```

Et c'est gagné !

Note: une version plus courte qui génère un grep pour chaque paire de caractère :

```bash
$ grep ^# enc|tr -d '#'|sed "s/\(..\)/grep '[^dev]::#.*\1' enc|cut -zd ':' -f3;/g"
grep '[^dev]::#.*8c' enc|cut -zd ':' -f3;grep '[^dev]::#.*15' enc|cut -zd ':' -f3;grep '[^dev]::#.*e8' enc|cut -zd ':' -f3;grep '[^dev]::#.*8a' enc|cut -zd ':' -f3;grep '[^dev]::#.*77' enc|cut -zd ':' -f3;grep '[^dev]::#.*5a' enc|cut -zd ':' -f3;grep '[^dev]::#.*92' enc|cut -zd ':' -f3;grep '[^dev]::#.*4d' enc|cut -zd ':' -f3;grep '[^dev]::#.*d0' enc|cut -zd ':' -f3;grep '[^dev]::#.*e8' enc|cut -zd ':' -f3;grep '[^dev]::#.*bb' enc|cut -zd ':' -f3;grep '[^dev]::#.*8c' enc|cut -zd ':' -f3;grep '[^dev]::#.*92' enc|cut -zd ':' -f3;grep '[^dev]::#.*d0' enc|cut -zd ':' -f3;grep '[^dev]::#.*15' enc|cut -zd ':' -f3;grep '[^dev]::#.*44' enc|cut -zd ':' -f3;grep '[^dev]::#.*77' enc|cut -zd ':' -f3;grep '[^dev]::#.*92' enc|cut -zd ':' -f3;grep '[^dev]::#.*b7' enc|cut -zd ':' -f3;grep '[^dev]::#.*77' enc|cut -zd ':' -f3;grep '[^dev]::#.*44' enc|cut -zd ':' -f3;grep '[^dev]::#.*92' enc|cut -zd ':' -f3;grep '[^dev]::#.*fd' enc|cut -zd ':' -f3;grep '[^dev]::#.*7f' enc|cut -zd ':' -f3;grep '[^dev]::#.*29' enc|cut -zd ':' -f3;grep '[^dev]::#.*e8' enc|cut -zd ':' -f3;

$ grep ^# enc|tr -d '#'|sed "s/\(..\)/grep '[^dev]::#.*\1' enc|cut -zd ':' -f3;/g" |sh|tr -d '^'
cust0m_b4sic_4u70_h07_k3ys%
```
