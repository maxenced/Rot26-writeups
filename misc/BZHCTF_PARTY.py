import binascii

one=int('0b0010001000101110001101110010100100111100001110000010111100001100001110000000011000001111001100000000000100011001001110010000100100100101',2)

two=int('0b0100000101000010010000110100010001000101010001100100011101001000010010010100101001001011010011000100110101001110010011110101000001010001',2)

three=int('0b0101000101011010010100110100010101000100010100100100011001010100010001110101100101001000010101010100101001001001010010110100111101001100',2)

four=int('0b0101000001001100010011110100101101001001010010100101010101001000010110010100011101010100010001100101010001000110010100100100010001000101',2)


xorlolz=one^two^three^four

print binascii.unhexlify('%x' % xorlolz) 
