# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from Crypto.Cipher import AES


def encrypt(key, data):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    encrypted_data, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return cipher.nonce, encrypted_data, tag


def decrypt(key, nonce, encrypted_data, tag):
    cipher = AES.new(
        key.encode('utf-8'), AES.MODE_EAX, nonce.encode('latin-1')
    )
    data = cipher.decrypt_and_verify(
        encrypted_data.encode('latin-1'), tag.encode('latin-1')
    )
    return data.decode('utf-8')
