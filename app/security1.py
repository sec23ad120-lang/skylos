from cryptography.fernet import Fernet

# Normally securely stored & loaded from environment/config
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(payload: str) -> str:
    return cipher_suite.encrypt(payload.encode()).decode()

def check_access(user: str, resource: str) -> bool:
    # Placeholder for access control logic (role-based, attribute-based)
    allowed_resources = {"admin": ["all"], "user": ["public_data"]}
    return resource in allowed_resources.get(user, [])
