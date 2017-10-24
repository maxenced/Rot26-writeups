# binary 2 one liner :

```bash
WINEDEBUG=+all ltrace -ff -s9999 /usr/lib/wine-development/wine LabyTime.exe 2>&1 |while read line ; do if [[ "$line" =~ "pan{" || "$line" =~ "PAN{" ]]; then FLAG=$(echo $line|sed 's#"# #g'|awk '{print $3}') ; curl -XPOST -d "flag=$FLAG" labytime.com -v; fi ; done
```
