import base64
import hashlib
from typing import Tuple
from Crypto.Cipher import AES


def encrypt(key: str, text: str) -> Tuple[str, str, str]:
    derived_key = hashlib.sha256(key.encode("utf-8")).digest()[:16]
    cipher = AES.new(derived_key, AES.MODE_EAX)
    encrypted_data, tag = cipher.encrypt_and_digest(text.encode("utf-8"))

    # Base64 encode the bytes to safe ASCII strings
    nonce_str = base64.b64encode(cipher.nonce).decode("utf-8")
    encrypted_str = base64.b64encode(encrypted_data).decode("utf-8")
    tag_str = base64.b64encode(tag).decode("utf-8")

    return nonce_str, encrypted_str, tag_str


def decrypt(key: str, nonce: str, encrypted_data: str, tag: str) -> str:
    derived_key = hashlib.sha256(key.encode("utf-8")).digest()[:16]

    # Base64 decode the strings back to bytes
    nonce_bytes = base64.b64decode(nonce.encode("utf-8"))
    encrypted_bytes = base64.b64decode(encrypted_data.encode("utf-8"))
    tag_bytes = base64.b64decode(tag.encode("utf-8"))

    cipher = AES.new(derived_key, AES.MODE_EAX, nonce_bytes)
    data = cipher.decrypt_and_verify(encrypted_bytes, tag_bytes)
    return data.decode("utf-8")
