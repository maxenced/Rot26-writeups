So, fun challenge.

What we have here is a table with some "random" data. The goal is to understand
how are the data generated, and find the one which don't match.  

Ex of data :

```
+----+----------+----------+
| id | value_0  | value_1  |
+----+----------+----------+
| 1  | soldiers | exchange |
| 2  | others   | solely   |
| 3  | helps    | fotos    |
| 4  | storage  | magnetic |
| 5  | customs  | arise    |
| 6  | devon    | wanted   |
| 7  | assault  | haven    |
| 8  | rouge    | below    |
| 9  | logging  | logging  |
| 10 | winning  | cover    |
+----+----------+----------+
```

This one is easy. Just find the word where `value_0 == value_1`.

Let's solve all of them :)

# Note

It appears that, for all the algorithm, we need to randomly find either :

 * the record which match
 * the record which *don't* match

So I wrote some code to always, for a given algorithm, check both :

```python
def apply_filter(challenge, filter_func):
    """ Filters the output of challenge entries using `filter_func`
    `filter_func` must return True or False
    Will return:
        * the id of the only record which match filters if there is only one
        or
        * the id of the only record which does *not* match filters if there is only one
        * None in all other cases
    """
    match = [ x for x in challenge if filter_func(x)]
    dont_match = [ x for x in challenge if not filter_func(x)]
    if len(match) == 1:
        return match[0]["id"]
    if len(dont_match) == 1:
        return dont_match[0]["id"]
    return None
```

# Word (don't) match 

So, the same as before, we can have either `value_0 == value_1` or `value_0 != value_1`.

Solved it with :

```python
def answer_find_same(challenge):
    """ Get the list of key/value and returns the id of the entry which has key = value
        If there is not exactly one entry, return None
    """
    name("value_0 == value_1")
    f = lambda x: x["values"][0] == x["values"][1]
    return apply_filter(challenge, f)
```

# (In)valid IP

```
+----+-----------------+
| id | value           |
+----+-----------------+
| 1  | 174.239.15.95   |
| 2  | 35.119.143.151  |
| 3  | 249.281.249.38  |
| 4  | 190.141.220.79  |
| 5  | 126.45.54.204   |
| 6  | 134.238.20.144  |
| 7  | 231.223.147.46  |
| 8  | 78.215.192.83   |
| 9  | 176.244.229.144 |
| 10 | 88.166.176.140  |
| 11 | 120.88.43.241   |
+----+-----------------+
```

I don't remember I had to find the only valid IP, but still, this function can handle both cases:

```python 
def answer_check_ip(challenge):
    """ Return the id of only invalid IP
    """
    name("valid ip")
    f = lambda x : not [ int(i) for i in x["values"][0].split('.') if int(i) > 255 ] # Return True if list is empty
    return apply_filter(challenge, f)
```

# Hashes

Exemple :
```
+----+----------+--------------------------------------------------------------------------------------------------+
| id | value_0  | value_1                                                                                          |
+----+----------+--------------------------------------------------------------------------------------------------+
| 1  | species  | 46c45bea012a4371780a89959e1c778b085e2b7602a64a1f17c34f4511b1ac53b3d75191f928a4f5ca85ccbbd1932bc8 |
| 2  | aging    | 824a27137d066ebfed14d475afc49dbd578f87daf0da184e7877a334869f2b8427aef7e97b0cbb24f364cf0f5128afe1 |
| 3  | voice    | 13c042cf28405fe3959c58797d579f26f6d3a3adca95b1c5b82c8c9470ef846ec11b8ebe7041fdf6a0c15d122c65fb7d |
| 4  | monitors | d339a6e3ec90d6a7500ba0e4497eeebe89be8d3018728f38e7542c8c9c588063b825675c14aa6adc9a1d9722c276c918 |
| 5  | literary | 238ddb9b01277df09af5fbd2f07c394b09ff6abe67478296833099c78fa0fe9e3e567d3c8413647f81efb32d37e46609 |
| 6  | permits  | 098f43f7ceb0d9a4ebd8c3e5de3ad77ceafbabab005a46e4ee7abe2bc4dc9a13187521f738671d206b7a33fa19787aea |
| 7  | dozen    | d4def1624c3a574363afb04289e47ebff0ba53182ce86e46de2d5771dc1678e1ad1f4e836243b7d2b85cd795b60fe917 |
| 8  | boats    | 9465b28f356c5af0ffd4ddb61bfed2e00adbf4b4ccb8ef1a3efcd68c70fe23548be9906eff3337e9d4a36e41656a4cfa |
| 9  | atlas    | 743e58d63c40458752631c3c7618ee664bc854c392121da6deba1d9414d4d57fff39e558130612bf6ce82e146905ee0f |
| 10 | should   | ae3eee435d34e34a62e6c132f525dddb9276faebfa8a39a029ab78f087d31f6298a9c8533d1068873cf76f037a68b9bc |
| 11 | sanyo    | ec3c5cd83b908be6f3818f265271e9d767d6a4c1f6ed350403a06d8ae7ca7b99321d85bc6fcee88445bb88d8dcdf6dd2 |
+----+----------+--------------------------------------------------------------------------------------------------+
```

I had a few different hashes (sha*, md5, etc). In order to avoid looking for
all of them, the function checks most of the available hash functions available
in hashlib.

```python
def check_hash(h, s):
    z = hashlib.new(h)
    z.update(s.encode('utf-8'))
    return z.hexdigest()

def check_hashes(challenge):
    """ Try all hashlib hashes function
    | 1  | utility  | 67b732dc42aaffa9056d34cc477c863c |
    """
    for h in ['md4','md5','ripemd160','sha','sha1','sha224','sha256','sha384','sha512','whirlpool']:
        name("valid hash {}".format(h))
        f = lambda x: check_hash(h, x["values"][0]) == x["values"][1]
        res =  apply_filter(challenge, f)
        if res is not None:
            return res
```

# CRC32 

Not much to say here. Sample was like :

```
+----+-------------------+------------+
| id | value_0           | value_1    |
+----+-------------------+------------+
| 1  | slovenia-flame    | 2794025826 |
| 2  | italia-musical    | 1601988563 |
| 3  | reliance-length   | 3984700778 |
| 4  | managing-largest  | 3865137473 |
| 5  | headset-entities  | 3276664454 |
| 6  | detector-restrict | 4052224228 |
| 7  | brings-insured    | 2197597317 |
| 8  | auckland-utility  | 2845994991 |
| 9  | major-fires       | 403591780  |
| 10 | wooden-links      | 643340853  |
| 11 | nursery-layout    | 511607902  |
| 12 | offering-monte    | 1192467455 |
| 13 | indexes-elements  | 1829548750 |
| 14 | packing-identify  | 1359052396 |
+----+-------------------+------------+
```

And I solved it with :

```python
def check_crc32(challenge):
    """ Check the CRC32 of value_0 vs value_1
    """
    name("CRC32")
    try:
        f = lambda x : int(crc32(x["values"][0].encode('utf-8'))) == int(x["values"][1])
        print(apply_filter(challenge, f))
        return apply_filter(challenge, f)
    except:
        return None
```

# Prime number 

Another easy one, just find the only prime/not prime number :

```
+----+-------+
| id | value |
+----+-------+
| 1  | 41756 |
| 2  | 88193 |
| 3  | 6179  |
| 4  | 93040 |
| 5  | 44109 |
| 6  | 77588 |
| 7  | 95949 |
| 8  | 67240 |
| 9  | 36826 |
| 10 | 44099 |
| 11 | 10853 |
| 12 | 52671 |
| 13 | 45972 |
+----+-------+
```

Solved it with:

```python
def check_prime(challenge):
    """ Check prime numbers
    """
    name("prime number")
    f = lambda x : is_prime(int(x["values"][0]),25)
    return apply_filter(challenge, f)
```

# RC4

In the status line (which didn't help us most of the time), we saw part of RC4 algorithm :

```
Status: for(c = 0; c < 256; c++) { i2 = (k[i1] + s[c] + i2) % 256; swap(&s[c], &s[i2]); i1 = (i1 + 1) % len; }
```

and the result was base64 encoded:

```
+----+----------------------------+--------------------------------------+
| id | value_0                    | value_1                              |
+----+----------------------------+--------------------------------------+
| 1  | rangers-lanka-centres      | QxeqoVu9N52nQUpZT2hZQmjIFSsf         |
| 2  | karma-neighbor-electric    | vsb/gxr0XZWGx/ACy2KUq7AdPb1p3Ig=     |
| 3  | contacts-reprints-seeker   | UAbn2o9+m8rcc8fPwlvY7xWJhhG1f7qe     |
| 4  | medieval-variable-equipped | JSBWtqRnJaoAaAKCz9NLatsSqWH5BtbzEEg= |
| 5  | lance-workout-friend       | ytghGg0NMwPLcx8RH/kAGaokVPY=         |
| 6  | grade-lambda-stupid        | jr68d1pHkG8vGkSDOJ2pz/4g1Q==         |
| 7  | assumes-publicly-crossing  | xpxrbpUGW3/jFY+bmGfAzMj2bcefGd8F/w== |
| 8  | hindu-cache-dealer         | oIzy1/TizirkUqZQXH7kYdLs             |
| 9  | stats-polymer-arrive       | QMoIsC0JMWueGoIrfrNsy8+UwdU=         |
| 10 | antiques-other-metro       | XH9/KaF8XePZuNG0zC8xUy2GKNs=         |
| 11 | bless-emerald-freebsd      | Rk43ZnQsQj+nBeUs+qZNsc2VOSVj         |
+----+----------------------------+--------------------------------------+
```

this is the algorithm which creates the permutation matrix in RC4. I used RC4 python implementation from [Wikipedia](https://fr.wikipedia.org/wiki/RC4) :

```python
def check_rc4(challenge):
    name("RC4")
    WikipediaARC4(challenge[0]["values"][0]).crypt(base64.b64decode(challenge[0]["values"][1]))
    f = lambda x : x["values"][0] == WikipediaARC4(x["values"][0]).crypt(base64.b64decode(x["values"][1]))
    return apply_filter(challenge, f)
```

# Hex alphabet

This one was a bit more complicated to implement. We had examples like :

```
+----+-----------------+--------------------------------+
| id | value_0         | value_1                        |
+----+-----------------+--------------------------------+
| 1  | myanmarsticks   | 92869e91929e8d8c8b969c948c     |
| 2  | parcelstreet    | 8f9e8d9c9a938c8b8d9a9a8b       |
| 3  | shapescurious   | 8c979e8f9a8c9c8a8d96908a8c     |
| 4  | fortypalace     | 99908d8b868f9e939e9c9a         |
| 5  | wickedoffline   | 88969c949a9b9099999396919a     |
| 6  | parentrefined   | bcadbea9a2b8bea9aaa5a2a9a8     |
| 7  | scottishcounted | 8c9c908b8b968c979c908a918b9a9b |
| 8  | middleexceed    | 92969b9b939a9a879c9a9a9b       |
| 9  | feedsferry      | 999a9a9b8c999a8d8d86           |
| 10 | edgarcentre     | 9a9b989e8d9c9a918b8d9a         |
| 11 | therebyholdem   | 8b979a8d9a9d869790939b9a92     |
+----+-----------------+--------------------------------+
```

We can see that 'a' seems to be 0x9e, 'b' = 0x9d etc ... After I got more samples, it looked like a is not always equal to 0x9e.
So I had to find the value for 'a', then ensure each letter match the correct value .

Code is (with some checks to avoid matching other hex-looking samples):

```python
def three_words_hex_value(challenge):
    """ Solve array with lines like :
        | 1  | beatles derek formal   | 9d9a9e8b939a8cdf9b9a8d9a94df99908d929e93     |
    by mapping each letter to a hex value
        a = 9e, then each letter decrease the value by 1 (b = 9d, c = 9c)
    """
    name("Hex alphabet")

    try: # Check if value_1 column is hex
        foo = unhexlify(challenge[0]["values"][1])
    except:
        return None

    # ensure it contains at least some hex letter, not only numeric
    try:
        int(challenge[0]["values"][1])
        return None # return if it worked
    except:
        pass

    if "EAX" in challenge[0]["values"][0]:
        return None

    if len(challenge[0]["values"][0]) != len(challenge[0]["values"][1]) / 2:
        return None

    alphabet = string.ascii_lowercase
    a = None
    for line in challenge:
        if 'a' in line["values"][0]:
            a = unhexlify(line["values"][1])[line["values"][0].index('a')]
            break
    print("  `-> Found value %s for 'a'" % a)

    for line in challenge:
        v0 = line["values"][0]
        v1 = unhexlify(line["values"][1])
        i = 0
        #print(line)
        while i < len(v0):
            if v0[i] not in alphabet:
                i = i+1
                continue
            c_v1 = v1[i]
            c_v0 = a - alphabet.index(v0[i])
        #    print("v0 : %s ; v1 : %s" % (c_v0, c_v1))
            if c_v0 != c_v1:
                return line["id"]
            i = i+1
    return None
```

# Shellcode

This one was ... fun. We got samples like : 

```
+----+-------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id | value_0           | value_1                                                                                                                                                                                  |
+----+-------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1  | EAX == 0x4F625126 | 535657558becb8742cdc5d2d8c66d5574bebffc333d2bb65712123f7f38bca81c150769a858bc133d2bea0e3e49af7f68bc233d2bfbdc825e8f7f78bf281c6795988fe8bfe8bc7c95f5e5bc3                                 |
| 2  | EAX == 0x3F4553BA | 535657558becb82d121d5c4bebffc3351fab4aad33d2bb1b1a28eaf7f38bfa81ef3087bf228bf781f6adc455938bce81e9907fe0378bc133d2b91fac5f74f7f1bb0845766881c3f8ba8997755d8bc2c95f5e5bc3                 |
| 3  | EAX == 0x582FB43C | 5357558becb9ac18e26a81e9573570a54aebffc281e91cf095ed8bd981c36f4f4ecc8bfb81ef48f10a34bafec9911681f20d9b79c8795b8bc7354cefb3cf8bf881c710f682988bd78bc2bf44ebc7dd81c7bc143822477380c95f5bc3 |
| 4  | EAX == 0x0C93D68B | 535657558becb80bf7b14e05df3af61033d2bf5fd17b8ff7f78bca81c1a1a4ebac8bc133d2be95e1b14df7f68bc2c95f5e5bc3                                                                                   |
| 5  | EAX == 0xB1B85CD4 | 558becb86e05bfa82dd1d8269b2d85ca174e8bc881e93df003528bc105aa932ec835515913848bd08bc2c9c3                                                                                                 |
| 6  | EAX == 0xC26F8EC2 | 5357558becbbc5ab7cc681eb09f7a4f881c306da97f48bfb8bc7c95f5bc3                                                                                                                             |
| 7  | EAX == 0xE1BCABC5 | 535657558becbb2c107ea781eb2d1ea0e781eb3a4621de8bcb8bc1c95f5e5bc3                                                                                                                         |
| 8  | EAX == 0x53122F83 | 5657558becb8832f125333d2bf0c4ab058f7f78bc233d2b90a3134d6f7f14febffc78bf28bc6c95f5ec3                                                                                                     |
| 9  | EAX == 0x41BA5B03 | 5356558becb8d34eeeca05a9abc2bf35bb00e4048bf081c6f24e6ad881eeb6ee04258bc633d2bb6886245af7f3b9fb31d86581c105ce279a4173e18bc233d2beffcc9c4ff7f68bf28bc6c95e5bc3                             |
| 10 | EAX == 0x700059F8 | 5357558becbf9ca17a7181f7b3ea2de781ef85f506568bc7b91ba0362c81c1e55fc9d3751933d2b9ecc7b031f7f181ea2b5319dd8bc205c14e2b048bd881eb1f875f938bd381f2cd5b52d28bda8bc3c95f5bc3                   |
| 11 | EAX == 0x886C7A77 | 535657558becbbdf7d8dd981c3bff2d2c681c3a5f94b838bf381f6a03833cf8bc633d2b94a5fc33ff7f18bfa81ef8ebae8a48bcf8bc1c95f5e5bc3                                                                   |
| 12 | EAX == 0x0E7BD093 | 56558becb8d92027f733d2be0bb314bdf7f68bc235924b5f608bd081c2983f08b48bf281eebef09ddeba8c9422cf81f2b15f34ff78038bc633d2be9285d4cef7f68bc2055d5bc4de8bf08bc6c95ec3                           |
| 13 | EAX == 0xAA0A1940 | 535657558becbf5241e62c81f7a86cf0dd81f76c1d33d18bdf81c32868b6348bf381f6fe81d1fe8bd68bc2c95f5e5bc3                                                                                         |
| 14 | EAX == 0x6455E563 | 5356558becb8c21aaa1e33d2b94c2ba8d0f7f18bca81c11dbe45f68bf149ebffc181c60d1b474881c6b8f0aa2c8bde81ebc8082dc18bc32da4dd42668bd881ebd5181cfe8bd38bc2c95e5bc3                                 |
+----+-------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

After some digging, it appears that `value_1` is a shellcode, and that you have to exec it and check value of EAX at the end.

For this I:

 * parsed eax
 * injected some instructions in shellcode (right before epilogue) to print eax value 
 * put the shellcode in some C code
 * compile It
 * run it and get output 

Code looks like :

```python
def run_shellcode(line):
    """ Check shellcode stuff
    """
    print_sc="\x50\x31\xC0\x31\xD2\xB0\x04\xBB\x01\x00\x00\x00\x89\xE1\xB2\x04\xcd\x80" # SC to print $eax on stdout
    exec_src="""
#include<stdio.h>
#include<string.h>
unsigned char shellcode[] = "@SC@";
int main(int argc, char **argv) {
    int (*ret)() = (int(*)())shellcode;
    ret();
}"""
    eax=line["values"][0].split(' ')[-1].replace('0x','')
    sc_orig=unhexlify(line["values"][1])
    leave_index=(sc_orig.rfind(b'\xc9'))
    sc=(sc_orig[:leave_index].decode('latin') + print_sc + sc_orig[leave_index:].decode('latin'))
    sc=''.join(["\\x{:02x}".format(ord(x)) for x in list(sc)])
    with open('spawn.c','w') as f:
        f.write(exec_src.replace('@SC@',sc))
    call('gcc -m32 -z execstack -o spawn spawn.c',shell=True)
    ret=check_output('./spawn',shell=True)
    good = hexlify(p32(int(hexlify(ret),16))).upper().decode()
    return good == eax

def check_shellcode(challenge):
    if "EAX" not in challenge[0]["values"][0]:
        return None
    f = lambda x : run_shellcode(x)
    return apply_filter(challenge, f)
```

# Main 

Finally, the main code to run this super-solver was :

```python
def find_answer(challenge):
    check_result_list_1_value = [
        answer_check_ip,
        check_prime
    ]
    check_result_list_2_values = [
        answer_find_same,
        check_hashes,
        three_words_hex_value,
        check_crc32,
        base64_length,
        check_shellcode,
        check_rc4,
        check_entropy,
    ]

    list_to_process = {
        1: check_result_list_1_value,
        2: check_result_list_2_values,
    }
    nb_values = len(challenge[0]["values"])
    for check_func in list_to_process[nb_values]:
        res = check_func(challenge)
        if res is not None:
            return res
    return None

def main():
    while True:
        answer = input('Would you like to play a game? [yes|no]: ').lower()
        if answer[0] != 'y':
            break
        # Submit blank answer with 'new' session to get a new session.
        session = 'new'
        answer = None
        while True:
            # Just very basic rate limiting.
            time.sleep(1)

            response = requests.get(PLAY_URL.format(session, answer))
            response.raise_for_status()
            json = response.json()

            if json['flag'] is not None:
                print('Status: %s' % (json['status']))
                print('FLAG: %s' % (json['flag']))
                return
            if json['error']:
                print('Error: %s' % (json['status']))
                break
            session = json['session']
            if json['score'] > 0:
                print("Answer Accepted.")
                print('New Score: %s' % (json['score']))
                print('')
            print('Status: %s' % (json['status']))

            items = json['challenge']

            answer = find_answer(items)
            if answer is not None:
                print("Found answer %s" % (answer))
            if answer is None:
                answer = input('Answer ID: ')

if __name__ == '__main__':
    main()
```

