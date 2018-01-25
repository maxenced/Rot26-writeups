# PyJail

In this jail (sorry, forgot to get the jail code), we got only a '__bultins__'.

Playing during some time, we found that:

 * We don't have access to properties starting with '__'
 * We don't have `getattr` or `vals`
 * We *do* have access to `print` and, more interesting, we have an `open()` function available

After some more investigation, `open()` is in fact a wrapped by some other function, and especially:

```python
open('flag.txt').read()
```

raises an error saying that `I see that you are trying to get the flag`.

Hmm, wait ... `open()` works, `read()` or `readlines()` seems to work. Would it be so simple that the wrapper just checks the full flag is not returned ? 

Well, yes ... `open('flag.txt').read()[0]` works \o/.

That's an easy way to get the flag :

```python
[ print(open('flag.txt').read()[i]) for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26,27,28,29,30,31,32]]
```

And here is the flag: `ENSIBS{d0_No7_Bl4cKli5t_w1Th_1f}`
