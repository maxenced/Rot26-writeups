rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def rotl(value, shift):
    value &= 0xFFFFFFFF
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def s20_quarterround(y0, y1, y2, y3):
    y1 = y1 ^ rotl(y0 + y3, 7)
    y2 = y2 ^ rotl(y1 + y0, 9)
    y3 = y3 ^ rotl(y2 + y1, 13)
    y0 = y0 ^ rotl(y3 + y2, 18)

    return y0, y1, y2, y3

def s20_rowround(y):
    y[0],  y[1],  y[2],  y[3]  = s20_quarterround(y[0],  y[1],  y[2],  y[3])
    y[5],  y[6],  y[7],  y[4]  = s20_quarterround(y[5],  y[6],  y[7],  y[4])
    y[10], y[11], y[8],  y[9]  = s20_quarterround(y[10], y[11], y[8],  y[9])
    y[15], y[12], y[13], y[14] = s20_quarterround(y[15], y[12], y[13], y[14])

    return y

def s20_columnround(x):
    x[0],  x[4],  x[8],  x[12] = s20_quarterround(x[0],  x[4],  x[8],  x[12])
    x[5],  x[9],  x[13], x[1]  = s20_quarterround(x[5],  x[9],  x[13], x[1])
    x[10], x[14], x[2],  x[6]  = s20_quarterround(x[10], x[14], x[2],  x[6])
    x[15], x[3],  x[7],  x[11] = s20_quarterround(x[15], x[3],  x[7],  x[11])

    return x

def s20_doubleround(x):
    x = s20_columnround(x)
    x = s20_rowround(x)

    return x

def s20_littleendian(b):
    return (b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)) & 0xFFFFFFFF

def s20_rev_littleendian(w):
    b = [0] * 4
    b[0] = w & 0xFF
    b[1] = (w >> 8) & 0xFF
    b[2] = (w >> 16) & 0xFF
    b[3] = (w >> 24) & 0xFF

    return b

def s20_hash(seq):
    x = [0] * 16
    z = [0] * 16

    for i in range(16):
        x[i] = z[i] = s20_littleendian(seq[(4*i):(4*(i+1))])

    for i in range(10):
        z = s20_doubleround(z)

    for i in range(16):
        z[i] += x[i]
        b0, b1, b2, b3 = s20_rev_littleendian(z[i])
        pos = i*4
        seq[pos] = b0
        seq[pos+1] = b1
        seq[pos+2] = b2
        seq[pos+3] = b3

    return seq

def s20_expand32(k, n):
    o = ["expa", "nd 3", "2-by", "te k"]

    keystream = [0] * 64

    for i in range(0,64,20):
        for j in range(4):
            keystream[i + j] = ord(o[i/20][j])

    for i in range(16):
        keystream[4+i] = k[i]
        keystream[44+i] = k[i+16]
        keystream[24+i] = n[i]

    keystream = s20_hash(keystream)

    return keystream

def s20_crypt(key, nonce, si, data):
    key = [ord(c) for c in key]
    nonce = [ord(c) for c in nonce]
    
    n = [0] * 16

    for i in range(8):
        n[i] = nonce[i]

    if (si % 64) != 0:
        b0, b1, b2, b3 = s20_rev_littleendian(si / 64)
        n[8] = b0
        n[9] = b1
        n[10] = b2
        n[11] = b3

        keystream = s20_expand32(key, n)

    outp = ""

    for i, c in enumerate(data):
        if ((si+i) % 64) == 0:
            b0, b1, b2, b3 = s20_rev_littleendian((si+i) / 64)
            n[8] = b0
            n[9] = b1
            n[10] = b2
            n[11] = b3

            keystream = s20_expand32(key, n)

        outp += chr(ord(c) ^ keystream[(si+i) % 64])

    return outp
