from typing import Tuple
from Crypto.Cipher import AES


def encrypt(key: str, text: str) -> Tuple[bytes, bytes, bytes]:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    encrypted_data, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
    return cipher.nonce, encrypted_data, tag


def decrypt(key: str, nonce: str, encrypted_data: str, tag: str) -> str:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce.encode('utf-8'))
    data = cipher.decrypt_and_verify(encrypted_data.encode('utf-8'), tag.encode('utf-8'))
    return data.decode('utf-8')
