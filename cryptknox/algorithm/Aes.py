from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os

class Aes:
    MAGIC = b'Cryptknox'
    def __init__(self, key):
        self.key = key


    def con_key(self,salt,bit_len):
        kdf = Scrypt(
            salt=salt,
            length=bit_len//8, # Generate key based on the bit size(128,192,256)
            n=2**14,
            r=8,
            p=1
        )
        return kdf.derive(self.key.encode())
        

    def encrypt(self,content,bit_length=256):
        salt = os.urandom(16)
        
        nonce = os.urandom(12)
        
        key = self.con_key(salt,bit_length)
        aesgcm = AESGCM(key)
        enc = aesgcm.encrypt(nonce,content,self.MAGIC)

        return self.MAGIC + salt + nonce + enc
    

    def decrypt(self,enc_content, bit_length= 256):
        # Checking Magic Header
        if enc_content[:len(self.MAGIC)] != self.MAGIC or len(enc_content) < 37:
            raise ValueError("Invalid encrypted content...")
        # Spliting the enc_content
        salt = enc_content[9:25]
        nonce = enc_content[25:37]
        _enc = enc_content[37:]

        key = self.con_key(salt,bit_length)

        aesgcm = AESGCM(key)

        decrypt = aesgcm.decrypt(nonce, _enc, self.MAGIC)
        return decrypt
        
        

        
        
            