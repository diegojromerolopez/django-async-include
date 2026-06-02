import base64
import unittest
from async_include import crypto


class TestCrypto(unittest.TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        key = "supersecretkey"
        original_query = "SELECT * FROM users WHERE id = 1 AND name = 'Admin';"

        nonce, encrypted_sql, tag = crypto.encrypt(key=key, text=original_query)

        # Ensure returned values are strings
        self.assertIsInstance(nonce, str)
        self.assertIsInstance(encrypted_sql, str)
        self.assertIsInstance(tag, str)

        decrypted_query = crypto.decrypt(
            key=key,
            nonce=nonce,
            encrypted_data=encrypted_sql,
            tag=tag,
        )

        self.assertEqual(decrypted_query, original_query)

    def test_decrypt_with_high_byte_values(self):
        # Verify that roundtrip works correctly when encrypted bytes contain high-bytes (> 127).
        key = "anothersecret"
        query = "SELECT * FROM test;"

        # Keep encrypting until we get a set of cryptographic bytes containing high bytes (> 127).
        # This checks that our Base64 transport preserves the bytes.
        found_high_bytes = False
        for _ in range(50):
            nonce, encrypted_sql, tag = crypto.encrypt(key=key, text=query)

            # Base64 decode to examine the raw bytes
            nonce_bytes = base64.b64decode(nonce.encode("utf-8"))
            encrypted_bytes = base64.b64decode(encrypted_sql.encode("utf-8"))
            tag_bytes = base64.b64decode(tag.encode("utf-8"))

            if (
                any(b > 127 for b in nonce_bytes)
                or any(b > 127 for b in encrypted_bytes)
                or any(b > 127 for b in tag_bytes)
            ):
                found_high_bytes = True

                decrypted_query = crypto.decrypt(
                    key=key,
                    nonce=nonce,
                    encrypted_data=encrypted_sql,
                    tag=tag,
                )
                self.assertEqual(decrypted_query, query)
                break

        self.assertTrue(found_high_bytes, "Could not generate cryptographic bytes containing values > 127")
