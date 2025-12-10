import pytest
from cryptography.fernet import Fernet
from app.security.data_encryption import DataEncryption

def test_encrypt_decrypt():
    encryptor = DataEncryption()
    original_text = "Sensitive information"
    encrypted = encryptor.encrypt(original_text.encode())
    decrypted = encryptor.decrypt(encrypted).decode()
    assert decrypted == original_text

def test_encryption_differs_from_plaintext():
    encryptor = DataEncryption()
    original_text = "Sensitive information"
    encrypted = encryptor.encrypt(original_text.encode())
    assert encrypted != original_text.encode()

def test_key_is_consistent():
    key = Fernet.generate_key()
    encryptor1 = DataEncryption(key)
    encryptor2 = DataEncryption(key)
    data = b"Test data"
    assert encryptor2.decrypt(encryptor1.encrypt(data)) == data

