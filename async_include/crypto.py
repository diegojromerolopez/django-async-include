import hashlib
from typing import Tuple
from Crypto.Cipher import AES


def encrypt(key: str, text: str) -> Tuple[bytes, bytes, bytes]:
    derived_key = hashlib.sha256(key.encode('utf-8')).digest()[:16]
    cipher = AES.new(derived_key, AES.MODE_EAX)
    encrypted_data, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
    return cipher.nonce, encrypted_data, tag


def decrypt(key: str, nonce: str, encrypted_data: str, tag: str) -> str:
    derived_key = hashlib.sha256(key.encode('utf-8')).digest()[:16]
    cipher = AES.new(derived_key, AES.MODE_EAX, nonce.encode('utf-8'))
    data = cipher.decrypt_and_verify(encrypted_data.encode('utf-8'), tag.encode('utf-8'))
    return data.decode('utf-8')
