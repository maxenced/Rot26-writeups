import os
import hmac
import hashlib

""" Uncipher me : \x01@N\x02t\x1f60\xaf?\x1c\xf1\xadS\xe2\x9c\n\x97[\xaa\xf5\xd0\\\xd6\x86\xd7\x9e\xcaUr\\M\xc3Q\xae\x01e\x1e\xcbz\xbd\x8f\x89e^\xde'\xaa\xbf\xe4\x19\xe9\xef\x12r\xdb\xb0X\xff\\>\xa1\xad\x98\xa1+\xc6b\x11x\xb0#\xf2\xc3\xc6&\x0c\x87w\xfe\xf0\xd6)\xd8\xd8ox\xd1\xbaR\xf5V4\xab\xa7\x92
"""

class Crypto(object):
    """ Custom CBC cipher based on SHA256 HMAC.
    """

    def xor(self, m1, m2):
        return "".join([chr(ord(a)^ord(b)) for a, b in zip(m1,m2)])

    def generate_ks(self, m1, m2):
        return hmac.new(m1, m2, hashlib.sha256).digest()

    def pad_message(self, message, length=32):
        padding_length = length - (len(message) % length)
        return "%s%s" % (message, (chr(padding_length) * padding_length))

    def unpad_message(self, message):
        padding_length = ord(message[-1])
        return message[:-padding_length]

    def split_to_blocks(self, message, length=32):
        return [message[i:i+length] for i in range(0, len(message), length)]

    def cipher(self, key, message):
        padded_message = self.pad_message(message)
        iv = os.urandom(32)
        ks = self.generate_ks(iv, key)
        blocks = self.split_to_blocks(padded_message)
        cipher_message = ""
        for block in blocks:
            cipher_block = self.xor(ks, block)
            ks = cipher_block
            cipher_message = "%s%s" % (cipher_message, cipher_block)

        return "%s%s" % (iv, cipher_message)

    def uncipher(self, key, cipher):
        iv = cipher[:32]
        message = cipher[32:]
        ks = self.generate_ks(iv, key)
        blocks = self.split_to_blocks(message)
        message = ""
        for block in blocks:
            plain = self.xor(ks, block)
            message = "%s%s" % (message, plain)
            ks = block

        return self.unpad_message(message)

if __name__ == "__main__":
    message = "\x01@N\x02t\x1f60\xaf?\x1c\xf1\xadS\xe2\x9c\n\x97[\xaa\xf5\xd0\\\xd6\x86\xd7\x9e\xcaUr\\M\xc3Q\xae\x01e\x1e\xcbz\xbd\x8f\x89e^\xde'\xaa\xbf\xe4\x19\xe9\xef\x12r\xdb\xb0X\xff\\>\xa1\xad\x98\xa1+\xc6b\x11x\xb0#\xf2\xc3\xc6&\x0c\x87w\xfe\xf0\xd6)\xd8\xd8ox\xd1\xbaR\xf5V4\xab\xa7\x92"

    crypto = Crypto()
    cipher = crypto.cipher(key, message)
#    uncipher = crypto.uncipher(key, message)

    print "message : %s" % message
    print "cipher : %s" % repr(cipher)
#    print "uncipher : %s" % uncipher
