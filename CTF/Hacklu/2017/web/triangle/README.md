# Triangle

This one starts ou with a simple page, a flag input field, a button, and three pictures of conspiracy stuff. "It's gonna be an annoying SQLI isn't it" I thought to myself. Oh how I wish it were so simple.

Looking at the source we get our first surprise, three JS scripts loaded:
1. util.js
2. secret.js
3. unicorn.js

we'll come back to these.
We also get three arrays of numbers (well six, on for firefox, one for chrome)
And finally the login function.

The util.js script contains basic utilities, like stringtohex, load base64, general stuff but not so useful
The secret.js is mot intersting, we have three functions, the three that are used in the login function:
1. test_pw()
2. enc_pw()
3. get_pw()

get_pw() is going to be useful, thanks to console.log() we can easily get it.
It uses the o3 array to get bytes from the templar image that we saw on the index page to generate the password.
So we have the password! `XYzaSAAX_PBssisodjsal_sSUVWZYYYb`

"Not so fast!" says the challenge, the other two functions call unicorn to create ARM emulated VMs
We can get around enc_pw() with console.log and a bit of bruteforcing. The chars can be entered one by one and the output isn't affected by letters entered afterwords.
I couldn't be bothered to code this so I did it by hand.
By feeding enc_pw() `RSr[M:9OYI<mmbkf^dmXfYkJOOQQSRQY` we get the password value out.
Aha simple, obviously nothing evil and nasty will be done in test_pw() (/s)

Ok, so that doesn't flag it, test_pw() does something to it and I can't bruteforce this one.
Lets look at the function:
```
function test_pw(e,_)
{
  var t=stoh(atob(getBase64Image("eye"))),r=4096,m=8192,R=12288,a=new uc.Unicorn(uc.ARCH_ARM,uc.MODE_ARM);
  a.reg_write_i32(uc.ARM_REG_R9,m),a.reg_write_i32(uc.ARM_REG_R10,R),a.reg_write_i32(uc.ARM_REG_R8,_.length),a.mem_map(r,4096,uc.PROT_ALL);
  for(var o=0;o<o1.length;o++)
    a.mem_write(r+o,[t[o1[o]]]);
  a.mem_map(m,4096,uc.PROT_ALL),a.mem_write(m,stoh(_)),a.mem_map(R,4096,uc.PROT_ALL),a.mem_write(R,stoh(e));
  var u=r,c=r+o1.length;
  return a.emu_start(u,c,0,0),a.reg_read_i32(uc.ARM_REG_R5)
}
```

Simply put:
1. fill variable t with a string from an ascii representation of the binary value of the base64 encoded value of the eye image on the index page
2. assign a few other variables
3. create a new instance of the unicorn engine using an ARM architecture
4. write some values to the registers and map some memory
5. write the content of t into the mapped memory
6. map more memory spaces and write our password and guess into them
7. define more variables
8. run the instance and read a register

The important part here is step 5, the value of t is bytecode written to memory, that's the part we need to understand
By adding console.log in the for loop we get the bytecode in decimal, when converted to hex we can send it to a decompiler:

```
.data:00000000 09 00 a0 e1                      mov	r0, r9
.data:00000004 0a 10 a0 e1                      mov	r1, sl
.data:00000008 08 30 a0 e1                      mov	r3, r8
.data:0000000c 00 40 a0 e3                      mov	r4, #0
.data:00000010 00 50 a0 e3                      mov	r5, #0
.data:00000014 00 c0 a0 e3                      mov	ip, #0
.data:00000018 00 20 d0 e5                      ldrb	r2, [r0]
.data:0000001c 00 60 d1 e5                      ldrb	r6, [r1]
.data:00000020 05 60 86 e2                      add	r6, r6, #5
.data:00000024 01 c0 04 e2                      and	ip, r4, #1
.data:00000028 00 00 5c e3                      cmp	ip, #0
.data:0000002c 00 00 00 0a                      beq	0x00000034
.data:00000030 03 60 46 e2                      sub	r6, r6, #3
.data:00000034 06 00 52 e1                      cmp	r2, r6
.data:00000038 05 00 00 1a                      bne	0x00000054
.data:0000003c 01 00 80 e2                      add	r0, r0, #1
.data:00000040 01 10 81 e2                      add	r1, r1, #1
.data:00000044 01 40 84 e2                      add	r4, r4, #1
.data:00000048 03 00 54 e1                      cmp	r4, r3
.data:0000004c f1 ff ff ba                      blt	0x00000018
.data:00000050 01 50 a0 e3                      mov	r5, #1
.data:00000054 00 00 a0 e3                      mov	r0, #0
.data:00000058 00 10 a0 e3                      mov	r1, #0
.data:0000005c 00 20 a0 e3                      mov	r2, #0
.data:00000060 00 30 a0 e3                      mov	r3, #0
.data:00000064 00 40 a0 e3                      mov	r4, #0
.data:00000068 00 60 a0 e3                      mov	r6, #0
.data:0000006c 00 70 a0 e3                      mov	r7, #0
.data:00000070 00 80 a0 e3                      mov	r8, #0
.data:00000074 00 90 a0 e3                      mov	r9, #0
.data:00000078 00 a0 a0 e3                      mov	sl, #0
.data:0000007c 00 c0 a0 e3                      mov	ip, #0
```

Although I'm rubbish at assembly, this code is not that complex, in essence:

```
It takes the password that was in register r9, puts it in r0
Puts our guess that was in register r10 (sl here), puts it in r1
R8 is the password length, that gets put into r3
R4, r5 and ip are set to zero (r5 is the register that needs to be set to 1 for the flag)
It loads the leftmost letter from the password and guess
It then add 5 to the guess
Does a logical AND between r4 and #1, puts the result in ip
if ip is NOT at zero
Substract 3 from guess
compare modified guess and password values
if they don't match exit, if they do move on to the next letter
```

So we add 5 to each letter and every other letter substract 3.

Knowing the actual password we need we can now reverse this:
```
pass = "XYzaSAAX_PBssisodjsal_sSUVWZYYYb"
R4 = False
for let in pass:
    if R4:
        print chr(ord(let)-5+3),
        R4 = False
    else:
        print chr(ord(let)-5),
        R4 = True
```

This still needs to be sent through enc_pw() but that takes only a few minutes, we then get the atual flag:
MPmVH94PTH7hhafgYahYaVfKJNLRNQLZ

Maybe some day get around to reversing enc_pw, it seems to be quite similar to test_pw, but today is not that day.
