import json
import os
import hashlib
import secrets

MASTER_FILE = "master.json"


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    ).hex()


def setup_master_password(password):
    salt = secrets.token_bytes(16)

    data = {
        "salt": salt.hex(),
        "password_hash": hash_password(password, salt)
    }

    with open(MASTER_FILE, "w") as file:
        json.dump(data, file)


def verify_master_password(password):
    if not os.path.exists(MASTER_FILE):
        return False

    with open(MASTER_FILE, "r") as file:
        data = json.load(file)

    salt = bytes.fromhex(data["salt"])

    return hash_password(password, salt) == data["password_hash"]


def get_salt():
    with open(MASTER_FILE, "r") as file:
        data = json.load(file)

    return bytes.fromhex(data["salt"])