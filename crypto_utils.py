from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(password.encode())
    )

    return Fernet(key)


def encrypt_password(password, master_password, salt):
    cipher = derive_key(master_password, salt)
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password, master_password, salt):
    cipher = derive_key(master_password, salt)
    return cipher.decrypt(
        encrypted_password.encode()
    ).decode()