SHA1
====

So we just get a sha1 : `05d3693c0781227771b97a9e3cf972d44c2d4439` and the hint that 'the first char is a digit'.

After a quick check on online database, it looks like we need to crack it.

First hope there is no special char, and try only uppercase/lowercase/digits.

We run JTR with custom mask and some threads:

```bash
$ echo 'admin:05d3693c0781227771b97a9e3cf972d44c2d4439 > hash'
$ ./john -max-len=10 -mask="?d[a-zA-Z0-9]" --format=Raw-SHA1 --fork=32 hash
```

And after some time:

```
$ ./john --show hash
admin:1stOrder

1 password hash cracked, 0 left
```

Note : BF in CTF has nothing really interesting. The challenge had a few hints
to restrict the pattern, which would have saved us some time.

