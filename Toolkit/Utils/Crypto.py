import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
class using:
    def base(password:str=""):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        return f
    def encrypt(phrase:str,letter:str):
        b=using.base(phrase)
        f=b.encrypt(letter)
        return f.decode()
    def decrypt(phrase:str,letter:str):
        b=using.base(phrase)
        f=b.decrypt(letter)
        return f.decode()