# app/security/data_encryption.py

from cryptography.fernet import Fernet
from typing import Optional

class DataEncryption:
    def __init__(self, key: Optional[bytes] = None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: bytes) -> bytes:
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.cipher.decrypt(ciphertext)

    def get_key(self) -> bytes:
        return self.key

# Usage example
if __name__ == "__main__":
    encryptor = DataEncryption()
    secret = b"My secret data"
    encrypted = encryptor.encrypt(secret)
    print(f"Encrypted: {encrypted}")
    decrypted = encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
